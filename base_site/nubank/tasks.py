from datetime import datetime
from datetime import timezone
from decimal import Decimal
from typing import List
from typing import Optional

from django.db import transaction
from django.db.models import Q

from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import Records
from base_site.nubank.models import NubankBankStatement
from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankItemSetup
from base_site.nubank.models import NubankStatement
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from slugify import slugify


def process_nubank_statements():
    statements = NubankStatement.objects.filter(is_processed=False).all()

    for s in statements:
        with transaction.atomic():
            split_statements_and_create_records(s)


def split_statements_and_create_records(s: NubankStatement):

    setup = get_setup(s.description)

    if setup:
        _update_statement(s)

        values_and_date = get_values_and_dates(s)

        for item in values_and_date:
            create_records(item["value"], s.description, s.item_time, item["date"], setup)


def _update_statement(s: NubankStatement) -> None:
    s.is_processed = True
    s.save()


def get_setup(
    description: str, name: Optional[FamilyMember] = None, value: Optional[int] = None
) -> Optional[NubankItemSetup]:

    slug_description = slugify(description, replacements=[["*", ""]])

    qs_setup = NubankItemSetup.objects.filter(description_slug=slug_description).filter(
        Q(check_name=name) | Q(check_name__isnull=True)
    )

    if not value:
        return qs_setup.first()

    setup = qs_setup.filter(check_value__gt=value, check_value_operator="<").first()
    if setup:
        return setup

    setup = qs_setup.filter(check_value__lt=value, check_value_operator=">").first()
    if setup:
        return setup

    setup = qs_setup.filter(check_value=value, check_value_operator="=").first()
    if setup:
        return setup

    return None


def get_values_and_dates(s: NubankStatement) -> List:

    registers = []
    first_date = calculate_record_date(s.item_time)
    if s.details.get("charges"):
        count = s.details.get("charges").get("count")
        amount = s.details.get("charges").get("amount")

        for n in range(count):
            next_date = first_date + relativedelta(months=n)
            registers.append({"date": next_date, "value": Decimal(amount) / 100})

    else:
        registers.append({"date": first_date, "value": s.amount})

    return registers


def create_records(debit: Decimal, description: str, item_date_create, item_date_executed, setup: NubankItemSetup):

    if setup:
        Records.objects.create(
            create_date_time=item_date_create,
            payment_date_time=item_date_executed,
            debit=debit,
            category=setup.category,
            name=setup.name,
            type_entry=setup.type_entry,
            description=description,
        )


def calculate_record_date(item_date):

    if item_date.day >= 8:
        next_month = item_date + relativedelta(months=1)
        return datetime.strptime(f"15/{next_month.month}/{next_month.year}", "%d/%m/%Y")
    else:
        return datetime.strptime(f"15/{item_date.month}/{item_date.year}", "%d/%m/%Y")


def process_nubank_bank_statements():
    statements = NubankBankStatement.objects.filter(is_processed=False).all()

    for s in statements:
        card = NubankCards.objects.filter(cpf=s.cpf).first()

        setup = get_setup(s.title, card.name, s.amount)

        if not (s.is_credit() or s.is_debit()):
            continue

        if setup:
            with transaction.atomic():

                Records.objects.create(
                    create_date_time=s.post_date,
                    payment_date_time=s.post_date,
                    debit=s.amount if s.is_debit() else None,
                    credit=s.amount if s.is_credit() else None,
                    category=setup.category,
                    name=setup.name,
                    type_entry=setup.type_entry,
                    description=s.title,
                )

                s.is_processed = True
                s.save()
