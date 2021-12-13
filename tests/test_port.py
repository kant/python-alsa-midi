
from alsa_midi import SequencerClient, SequencerPort


def test_port_create_close():
    client = SequencerClient("test_c")
    port = client.create_port("test_p")

    assert isinstance(port, SequencerPort)
    assert port.client is client

    port.close()

    assert port.client is None

    # should do nothing now
    del port


def test_port_create_del():
    client = SequencerClient("test_c")
    port = client.create_port("test_p")

    assert isinstance(port, SequencerPort)
    assert port.client is client

    del port


def test_port_create_close_alsa(alsa_seq_state):
    client = SequencerClient("test_c")
    port = client.create_port("test_p")

    alsa_seq_state.load()
    assert (port.client_id, port.port_id) in alsa_seq_state.ports
    alsa_port = alsa_seq_state.ports[port.client_id, port.port_id]

    assert alsa_port.name == "test_p"
    assert "RWe" in alsa_port.flags

    port.close()

    alsa_seq_state.load()
    assert (port.client_id, port.port_id) not in alsa_seq_state.ports


def test_port_create_del_alsa(alsa_seq_state):
    client = SequencerClient("test_c")
    port = client.create_port("test_p")

    client_id, port_id = port.client_id, port.port_id

    alsa_seq_state.load()
    assert (client_id, port_id) in alsa_seq_state.ports
    alsa_port = alsa_seq_state.ports[client_id, port_id]

    assert alsa_port.name == "test_p"
    assert "RWe" in alsa_port.flags

    del port

    alsa_seq_state.load()
    assert (client_id, port_id) not in alsa_seq_state.ports