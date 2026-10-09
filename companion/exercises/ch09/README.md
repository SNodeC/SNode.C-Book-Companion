# Chapter 9 — solutions and discussion

## 1. Review (O1)

The device address identifies the peer, while the selected service is specific to
the Bluetooth family. Channel 16 names an RFCOMM service; an L2CAP PSM names an
L2CAP service. Changing `rc` to `l2` does not create a corresponding listener or
convert its protocol. Discover or configure the actual service, match its family
and selector, then decide whether the same byte protocol can be reused.

## 2. Review (O2)

First check that the installed public components and development dependencies are
available. Then inspect the selected controller, power/radio-blocking state,
compatible peer hardware and Bluetooth Classic service. Inspect the device
relationship and any pairing/authorization required by the service policy. Start
the intended peer application and verify its local device/selector. Observe
activation status before debugging application framing. A paired device and a
built program do not establish that this particular service is listening.

## 3. Lab (O1)

After [the common configuration](../README.md):

```sh
cmake --build build/labs --target ch09-lab
ctest --test-dir build/labs -R '^exercise-ch09-selectors$' --output-on-failure -V
```

This hardware-independent lab requires the installed RFCOMM/L2CAP legacy stream
components and Bluetooth development support (BlueZ headers/libraries on Linux).
It opens no radio socket. The public address classes initially expose an empty
configured device string and zero selectors. The solution then sets one device
address with RFCOMM channel 16 and L2CAP PSM `0x1001`, initializes both address
objects, and checks that their getters retain those choices. Expect default-field
output, two rendered addresses, and a PASS naming channel 16 and PSM 4097.

An explicit all-zero device address denotes a wildcard; it is not the initial
configured string returned by `getBtAddress()`. Nor is either form a discovered
remote service. The assertions test public field behavior and representation;
they do not establish controller availability, pairing, binding or delivery.

### Optional equipped extension: physical RFCOMM exchange

This additional observation requires two Linux hosts with compatible enabled
Bluetooth Classic controllers, radio range, appropriate permissions, matching
service policy, and any required pairing/authorization. Follow the chapter's
controller/preparation sequence first. Do not run against an unrelated device.
The `endpoint-rc` and `endpoint-l2` drivers are built by `ch09-lab`; each reuses
`family-server.cpp` and the canonical EchoPair context. The commands below exercise
RFCOMM only; they do not certify L2CAP.

On the server host, choose an available channel (16 below) and bind the intended
adapter address. Use a private configuration directory for this run:

```sh
lab_config=$(mktemp -d)
mkdir -m 700 "$lab_config/config" "$lab_config/state" "$lab_config/runtime"
XDG_CONFIG_HOME="$lab_config/config" XDG_STATE_HOME="$lab_config/state" \
  XDG_RUNTIME_DIR="$lab_config/runtime" \
  build/labs/companion/exercises/ch09/endpoint-rc \
  endpoint local --host="$LOCAL_BT_ADDRESS" --channel=16
rm -r "$lab_config"
```

Set `LOCAL_BT_ADDRESS` to that host's controller address before running. Wait for
`BOUND`, then from the prepared peer host set `PEER_BT_ADDRESS` to the server's
controller address and run:

```sh
python3 - "$PEER_BT_ADDRESS" <<'PY'
import socket, sys
payload = b'900,23.5\n'
with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as peer:
    peer.settimeout(10)
    peer.connect((sys.argv[1], 16))
    peer.sendall(payload)
    reply = b''
    while len(reply) < len(payload):
        part = peer.recv(len(payload) - len(reply))
        if not part:
            raise RuntimeError('EOF before complete echo')
        reply += part
    assert reply == payload
    print('PASS: physical RFCOMM exact byte exchange')
PY
```

Stop the server with Ctrl-C after the exchange. Expected evidence is `BOUND`, an
actual connection identity, and an exact reply, not merely a “paired” indication.
The server driver compiles in ordinary CI, but this physical observation requires
an equipped run. If hardware is unavailable, complete the selector lab and local
checkpoint; explicitly leave radio delivery unverified. The lab sends no model
acceptance command and implements no measurement parser.

## 4. Lab (O3): Part III checkpoint

```sh
ctest --test-dir build/labs -R '^exercise-ch09-part-checkpoint$' --output-on-failure -V
```

The same bounded fixture runs the canonical byte protocol first over IPv4 loopback
and then through a private Unix path. It sends identical measurement-shaped bytes,
including invalid binary input, and requires an exact reply in both cases. Actual
producer/service identities must agree with the server's observations in opposite
directions. On Unix, the producer removes its own path, the server removes its
service path during shutdown, and an unrelated file survives. These checks occur
before the temporary directory is removed. Expect one PASS per carrier.

A local helper with controlled directory access may favor a Unix path; existing
network tools or a future remote producer may favor IP. Name the corresponding
exposure, identity, namespace, and cleanup obligations. Echoing sequence 900 does
not assign accepted sequence 1: transport still precedes framing, validation, and
the shared model's acceptance. This checkpoint makes no Bluetooth-delivery claim.

## 5. Design (O2, O3)

A BLE advertisement does not establish an RFCOMM or L2CAP stream service of the
kind used here. Obtain the sensor's actual service/protocol description and a
compatible supported input adapter before choosing a transport. The local helper
is already a pathname-stream candidate, but still needs endpoint access policy,
framing and validation. Translate valid records into the same shared model rather
than treating each carrier as another owner of accepted state.

Keep device preparation, byte delivery, protocol decoding, and domain acceptance
as separate observations. If an adapter is needed, its design must define data
conversion and failure behavior; changing a namespace is insufficient. No radio
availability can be inferred from the local checkpoint.
