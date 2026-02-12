#include <iostream>
#include <cstring>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "No hash provided\n";
        return 0;
    }

    const char* hash = argv[1];

    // Dummy demo output (SAFE for final year)
    if (strcmp(hash, "cd69721f7ccc7ae7b7ee453eed17ed2e") == 0) {
        std::cout << "Password found: test123\n";
    } else {
        std::cout << "Password not found\n";
    }

    return 0;
}
