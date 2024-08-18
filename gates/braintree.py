import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id='r4szgmn9v43f33q4',
        public_key='hdmg628hcj37p3tb',
        private_key='5d8f331d4c05f848b8486688b6735602'
    )
)

# Función para verificar una tarjeta de crédito
def check_credit_card(ccn, mm, yy, cvv, message):
    from handlers.command_handlers import *
    card_number = ccn
    expiration_date = mm + yy
    result = gateway.transaction.sale({
        "amount": "0.01",  # Monto pequeño para verificar la tarjeta
        "credit_card": {
            "number": card_number,
            "expiration_date": expiration_date,
            "cvv": cvv
        },
        "options": {
            "submit_for_settlement": False  # No se procesa para liquidación
        }
    })

    if result.is_success:
        msg = "APROBADA"
        respuesta = "Transacción exitosa"
    else:
        msg = "DECLINADA"
        respuesta = ", ".join([error.message for error in result.errors.deep_errors])

    return msg, respuesta
