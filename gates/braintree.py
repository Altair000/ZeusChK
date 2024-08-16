import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id='your_merchant_id',
        public_key='your_public_key',
        private_key='your_private_key'
    )
)

# Función para verificar una tarjeta de crédito
def check_credit_card(card_number, expiration_date, cvv):
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
