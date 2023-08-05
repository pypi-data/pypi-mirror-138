#-*- coding: utf-8 -*-
import sys

sys.path.append('/Users/robertoneves/Projetos/moippy')

import moippy

def main(arg):

    moippy.Juno('4E1574938F3DD69306BC336E348276ACC9CBE72B4E8396B2520436663C66C08E', '9OuOfYM2QZRhmUug', 'gw<Nl6bc2Ib,VX&)c2U{mX1?d_zEg0^d', sandbox=True)


    



        # cartao_bandeira: "mastercard"
        # cartao_final: "8884"
        # cartao_hash: "107438d9-4459-41d6-8608-af469a684ba6"
        # cartao_holder: "louise chiabai bortolini"
        # cartao_holder_cpf: "12451557761"
        # cartao_validade: "022026"

        #{'creditCardId': '9a453d71-3ec1-44a5-b2f3-0596ced42a35', 'last4CardNumber': '1112', 'expirationMonth': '2', 'expirationYear': '2026'}
        #{'creditCardId': '8c4449ea-ba70-4e9c-b9e4-3189efc22196', 'last4CardNumber': '8884', 'expirationMonth': '12', 'expirationYear': '2026'}


    #[{'id': 'chr_57EFAA34970F82A5953EA685C23E6DF3', 'code': 136606778, 'reference': '', 'dueDate': 'iso', 'link': 'https://pay-sandbox.juno.com.br/charge/boleto.pdf?token=1336909:m:fec0534e339bc196d939ca89ea4df0279e91ed7329c8bbe19395a9da189747b9', 'checkoutUrl': 'https://pay-sandbox.juno.com.br/checkout/D08586A38C0683D4286690BFB2B33B3EDE8F00031460F139', 'installmentLink': 'https://pay-sandbox.juno.com.br/charge/boleto.pdf?token=136606778:7c12969479062d1531d0bb86ea8d1a0093603d01a7af989da36241b232cd5c06', 'payNumber': 'BOLETO TESTE - Não é válido para pagamento', 'amount': 10.0, 'status': 'ACTIVE', 'billetDetails': {'bankAccount': '0001/1000025816-1', 'ourNumber': '000000136606778-6', 'barcodeNumber': '38396867700000010000000258160000001366067781', 'portfolio': '0001'}}]
    # {'_embedded': {'charges': [{'id': 'chr_5BF3EFDF36AE26E72A7659B60CD6B518', 'code': 136606768, 'reference': '', 'dueDate': '2021-07-10', 'link': 'https://pay-sandbox.juno.com.br/charge/boleto.pdf?token=1336899:m:e2d9b6caadebc1f9d549a6b1777bf92134f94a0941a3f6f356e5161eb3575f06', 'checkoutUrl': 'https://pay-sandbox.juno.com.br/checkout/2A638CDD646E92073CE5E3F9F0121F15E4621B7861E0D7D3', 'installmentLink': 'https://pay-sandbox.juno.com.br/charge/boleto.pdf?token=136606768:4771c57ce10484793f0fe0392c949fe85acdcee51dfc7886393a8b352b15f83d', 'payNumber': 'BOLETO TESTE - Não é válido para pagamento', 'amount': 10.0, 'status': 'ACTIVE', 'billetDetails': {'bankAccount': '0001/1000025816-1', 'ourNumber': '000000136606768-9', 'barcodeNumber': '38391867700000010000000258160000001366067681', 'portfolio': '0001'}, '_links': {'self': {'href': 'https://sandbox.boletobancario.com/api-integration/charges/chr_5BF3EFDF36AE26E72A7659B60CD6B518'}}}]}}

    #{'type': 'PAYMENT', 'name': 'Louise Chiabai Bortolini', 'motherName': 'Rosangela Chiabai', 'document': '12451557761', 'email': 'louise@agenciabrava.com.br', 'birthDate': '1986-07-16', 'phone': '27999191566', 'businessArea': 2015, 'linesOfBusiness': 'Pessoa Física - Digital Influencer', 'address': {'street': 'Desembargador Euripedes Queiroz do Valle', 'number': '301', 'complement': 'Ap 802', 'neighborhood': 'Jardim Camburi', 'city': 'Vitória', 'state': 'ES', 'postCode': '29090090'}, 'bankAccount': {'bankNumber': '033', 'agencyNumber': '4316', 'accountNumber': '010016473', 'accountComplementNumber': '0', 'accountType': 'CHECKING', 'accountHolder': {'name': 'Louise Chiabai Bortolini', 'document': '12451557761'}}, 'emailOptOut': False, 'autoTransfer': False, 'socialName': False, 'monthlyIncomeOrRevenue': 5000, 'id': 'dac_E6FECDB17EAC5992', 'status': 'AWAITING_DOCUMENTS', 'createdOn': '2021-07-08T14:57:14.451000-03:00', 'resourceToken': '8A596ED1DEB738091FDE8AF11CCD6E7730970A95503AB32CEA340FAB190139C9'}

if __name__ == "__main__":
    main(sys.argv)
