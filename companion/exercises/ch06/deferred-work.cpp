#include <core/EventReceiver.h>
#include <core/SNodeC.h>
#include <iostream>
#include <vector>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    std::vector<int> trace;
    bool firstActive = false;
    bool childDeferred = false;
    bool running = false;
    core::EventReceiver::atNextTick([&] {
        running = core::SNodeC::state() == core::State::RUNNING;
        firstActive = true;
        trace.push_back(1);
        core::EventReceiver::atNextTick([&] {
            childDeferred = !firstActive;
            trace.push_back(3);
            core::SNodeC::stop();
        });
        trace.push_back(2);
        firstActive = false;
    });
    // All captures remain alive through start() and coordinated shutdown.
    if (!trace.empty()) {
        std::cerr << "Callback ran on the registration stack\n";
        return 1;
    }
    const int status = core::SNodeC::start();
    if (status != 0 || !running || !childDeferred || trace != std::vector<int>{1, 2, 3}) {
        std::cerr << "Deferred dispatch or callback return order differs\n";
        return 1;
    }
    std::cout << "PASS: empty trace before start; RUNNING dispatch gives 1,2,3; child "
                 "sees first callback returned\n";
}
