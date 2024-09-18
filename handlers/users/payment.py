import logging

from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from filters.Filters import ExpiredSubscription
from services.GetMessage import get_mes
from services.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.photo, ExpiredSubscription())
async def payment(message: Message):
    prices = [LabeledPrice(label="XTR", amount=130)]
    await message.answer_invoice(
        title="Оплата",
        description="Ваш пакет закончился.\nЧтобы продолжить использовать бот, пожалуйста, оплатите пакет на месяц — это стоит всего 130 звезд и включает в себя проверку 50 блюд.",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=await Keyboards.payment_kb(),
    )


@router.pre_checkout_query()
async def success_pre_checkout_query(message: PreCheckoutQuery):
    await message.answer(ok=True)


@router.message(F.successful_payment)
async def success_payment_handler(message: Message):
    await message.answer(text=get_mes("success_payment"))


payment_rt = router
