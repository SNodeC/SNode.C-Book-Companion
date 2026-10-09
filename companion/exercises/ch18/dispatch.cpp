// A synchronous test route tree: observations belong to one sequential request.
#include <express/legacy/in/WebApp.h>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);
    const express::legacy::in::WebApp app("lab");
    const express::Router router;
    std::string trace;
    app.use([&](const auto& req, const auto&, express::Next& next) {
        trace = "app-before";
        std::cout << "APP " << req->originalUrl << std::endl;
        next();
    });
    app.use("/blocked", [](const auto&, const auto& res, express::Next&) {
        std::cout << "STOP" << std::endl;
        res->status(403)
            .set("X-Trace", "app-before,stop")
            .send("middleware stopped request");
    });
    app.get("/blocked", [](const auto&, const auto& res) {
        std::cout << "UNEXPECTED-HANDLER" << std::endl;
        res->send("unreachable");
    });
    router.use([&](const auto&, const auto&, express::Next& next) {
        trace += ",router-before";
        std::cout << "ROUTER" << std::endl;
        next();
    });
    router.get("/status", [&](const auto&, const auto& res) {
        trace += ",handler";
        std::cout << "HANDLER" << std::endl;
        res->set("X-Trace", trace).send(trace);
    });
    app.use("/api", router);
    app.listen([](const auto&, const auto&) {
    });
    return express::WebApp::start();
}
