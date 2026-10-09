#include <Log.h>
#include <system_error>

int main() {
    snode::log::Settings settings;
    settings.level = snode::log::Level::Info;
    settings.format = snode::log::Format::Json;
    settings.color = snode::log::ColorMode::Never;
    settings.componentLevels.push_back(
        {"gateway.measurements", snode::log::Level::Debug});
    snode::log::configure(settings);

    snode::log::Identity identity;
    identity.instance = "measurement-input";
    auto log = snode::log::application("gateway.measurements", identity);

    log.info("Measurement example initialized");
    log.event(snode::log::Level::Info,
              "measurement.accepted",
              "Accepted measurement sequence {}",
              1);
    log.debug() << "Diagnostic sequence " << 1;
    log.systemError(snode::log::Level::Warning,
                    std::make_error_code(std::errc::permission_denied),
                    "Demonstration error; no file operation was attempted");
}
