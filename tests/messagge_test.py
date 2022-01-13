from core.message import Message, MexType, MexPriority

VALUES_1 = {
    'text': 'Ciao',
    'message_priority': 3,
    'message_type': 0,
    'message_time': 3,
    'message_timeout': 7
}

VALUES_2 = {
    'text': 'Ciao',
    'message_priority': 4,
    'message_type': 1,
    'message_time': 5,
    'message_timeout': 10
}


class TestMessage:
    def test_create_message(self):
        message1 = Message('Ciao', MexPriority.medium, MexType.default, message_time=3, message_timeout=7)
        assert message1.values == VALUES_1

        message2 = Message('Ciao', MexPriority.high, MexType.trap)
        assert message2.values == VALUES_2

    def test_reduce_timeout_time(self):
        timeout = 10
        t = 8
        message = Message('Ciao', MexPriority.medium, MexType.default, message_time=t, message_timeout=timeout)
        for i in range(0, timeout):
            message.reduce_timeout()
            assert message.message_timeout == timeout-i-1
            assert message.message_timeout >= 0

            message.reduce_time()
            assert message.message_time == t-i-1
            # todo: non so se mettere anche questo assert => verificare da bob se serve o no
            # assert message.message_time >= 0
