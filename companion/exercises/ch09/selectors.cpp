#include <iostream>
#include <net/l2/SocketAddress.h>
#include <net/rc/SocketAddress.h>

int main() {
    net::rc::SocketAddress rfcomm;
    net::l2::SocketAddress l2cap;
    if (rfcomm.getChannel() != 0 || l2cap.getPsm() != 0 ||
        !rfcomm.getBtAddress().empty() || !l2cap.getBtAddress().empty()) {
        std::cerr << "Default configured device/selector differs\n";
        return 1;
    }
    std::cout << "Default: empty configured device string, zero selectors\n";
    const std::string device = "10:3D:1C:AC:BA:9C";
    rfcomm.setBtAddress(device).setChannel(16);
    l2cap.setBtAddress(device).setPsm(0x1001);
    rfcomm.init();
    l2cap.init();
    if (rfcomm.getBtAddress() != device || l2cap.getBtAddress() != device ||
        rfcomm.getChannel() != 16 || l2cap.getPsm() != 0x1001) {
        std::cerr << "Configured Bluetooth fields did not survive initialization\n";
        return 1;
    }
    std::cout
        << "RFCOMM " << rfcomm.toString() << '\n'
        << "L2CAP " << l2cap.toString() << '\n'
        << "PASS: one device; channel 16 and PSM 4097 (0x1001); no radio operation\n";
}
