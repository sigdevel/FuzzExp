#include "fuzzer/FuzzedDataProvider.h"
#include "../csv.h"
#include <iostream>
#include <sstream>
#include <chrono>
#include <thread>

enum class FuzzingErrorCode {
    NoError,
    InvalidInputSize,
    LineReaderError,
    CSVReaderError,
    TimeoutError
};

void reportError(FuzzingErrorCode errorCode, const std::string& errorMessage) {
    std::cerr << "Fuzzing Error: " << static_cast<int>(errorCode) << " - " << errorMessage << std::endl;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    if (size < 2 ) {
        reportError(FuzzingErrorCode::InvalidInputSize, "Размер входных данных не соответвует условиям");
        return static_cast<int>(FuzzingErrorCode::InvalidInputSize);
    }

    FuzzedDataProvider fdp(data, size);

    auto startTime = std::chrono::steady_clock::now();
   try {
        if (fdp.ConsumeBool()) {
            // Test the LineReader
            auto buff = fdp.ConsumeRemainingBytesAsString();
            io::LineReader reader{"fuzz.in", buff.c_str(), buff.c_str() + buff.size()};
            while (reader.next_line()) {
                // Perform necessary processing on each line

                // timer checker (default = 1)
                auto currentTime = std::chrono::steady_clock::now();
                auto elapsedSeconds = std::chrono::duration_cast<std::chrono::seconds>(currentTime - startTime).count();
                if (elapsedSeconds > 1) {
                    reportError(FuzzingErrorCode::TimeoutError, "Истечение таймера - пропуск семпла");
                    return static_cast<int>(FuzzingErrorCode::TimeoutError);
                }
            }
        } else {
            // Test the CSVReader
            auto buff = fdp.ConsumeRemainingBytesAsString();
            io::CSVReader<4, io::trim_chars<' '>, io::no_quote_escape<','>> in("fuzz.in", buff.c_str(), buff.c_str() + buff.size());
            int w;
            std::string x, y;
            double z;
            while (in.read_row(w, x, y, z)) {
                // Perform necessary processing on each row

                // Check if the code has been running for more than 10 seconds
                auto currentTime = std::chrono::steady_clock::now();
                auto elapsedSeconds = std::chrono::duration_cast<std::chrono::seconds>(currentTime - startTime).count();
                if (elapsedSeconds > 1) {
                    reportError(FuzzingErrorCode::TimeoutError, "Timeout occurred. Transitioning to next input sequence.");
                    return static_cast<int>(FuzzingErrorCode::TimeoutError);
                }
            }
        }
    } catch (const io::error::base& e) {
        if (fdp.ConsumeBool()) {
            reportError(FuzzingErrorCode::LineReaderError, e.what());
            return static_cast<int>(FuzzingErrorCode::LineReaderError);
        } else {
            reportError(FuzzingErrorCode::CSVReaderError, e.what());
            return static_cast<int>(FuzzingErrorCode::CSVReaderError);
        }
    }

    return static_cast<int>(FuzzingErrorCode::NoError);
}
