#include <string>
#include <iostream>
#include <fstream>

// includes classes
#include "../third_party/md5_hasher.hpp"

namespace ACPP
{
    namespace file_assists
    {
        std::string File_to_MD5(std::string path);
    }
}