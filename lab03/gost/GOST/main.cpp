#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include "GostCipher.h"

enum RETURN_CODES {
    SUCCESS = 0,
    NOT_ENOUGH_ARGS = 1,
    TOO_MANY_ARGS = 2,
    WRONG_OPERATION = 3,
    WRONG_KEY = 4,
    FAILED_TO_READ_FILE = 5,
    FAILED_TO_WRITE_FILE = 6,
};

std::vector<uint8_t> read_binary_file(const char* input) {
    try {
        std::ifstream file(input, std::ios::in | std::ios::binary);
        file.unsetf(std::ios::skipws);
        if (file.is_open()) {
            file.seekg(0, std::ios::end);
            const auto size = file.tellg();
            file.seekg(0, std::ios::beg);
            auto data = std::vector<uint8_t>();
            data.reserve(size);
            data.insert(
                data.cbegin(),
                std::istream_iterator<uint8_t>(file),
                std::istream_iterator<uint8_t>()
            );
            file.close();
            return data;
        }
    }
    catch (const std::exception& ex) {
        std::cerr << ex.what() << std::endl;
    }
    return {};
}

bool write_to_binary_file(const char* filename, const std::vector<uint8_t>& raw) {
    std::ofstream file(filename, std::ios::out | std::ios::binary);
    if (file.is_open()) {
        file.write((const char*)raw.data(), raw.size());
        file.flush();
        file.close();
        return true;
    }
    return false;
}

int main(int argc, char** argv)
{
    switch (argc) {
        case 0: case 1: case 2: case 3: case 4:
            return RETURN_CODES::NOT_ENOUGH_ARGS;
        case 5:
            if (strcmp(argv[1], "encrypt") != 0 && strcmp(argv[1], "decrypt") != 0) {
                return RETURN_CODES::WRONG_OPERATION;
            }

            std::cout << "Operation is valid. Loading key file..." << std::endl;

            auto key = read_binary_file(argv[2]);
            
            if (key.size() == 0) {
                return RETURN_CODES::FAILED_TO_READ_FILE;
            }

            if (key.size() != 32) {
                return RETURN_CODES::WRONG_KEY;
            }

            std::cout << "Key is fine. Loading input file..." << std::endl;

            auto input = read_binary_file(argv[3]);

            if (input.size() == 0) {
                return RETURN_CODES::FAILED_TO_READ_FILE;
            }

            const auto block_num = input.size() / 8;
            const auto to_add = input.size() % 8;
            for (int i = 0; i < to_add; ++i) {
                input.push_back(0);
            }

            std::cout << "Input is loaded. Encrypting..." << std::endl;

            auto cipher = GostCipher((const char*)key.data());

            if (strcmp(argv[1], "encrypt") == 0) {
                for (int i = 0; i < block_num; i += 8) {
                    cipher.encrypt(input.data());
                }
            }
            else {
                for (int i = 0; i < block_num; i += 8) {
                    cipher.decrypt(input.data());
                }
            }

            if (!write_to_binary_file(argv[4], input)) {
                return RETURN_CODES::FAILED_TO_WRITE_FILE;
            }

            std::cout << "Done!" << std::endl;
            return RETURN_CODES::SUCCESS;
    }

    return RETURN_CODES::TOO_MANY_ARGS;
}
