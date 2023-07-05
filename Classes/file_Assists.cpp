#include "file_Assists.hpp"


std::string ACPP::file_assists::File_to_MD5(std::string path)
{
    std::ifstream fp(path, std::ios_base::binary);
    char buffer[1024];

    fp.read(buffer, sizeof(buffer));
    
    for (std::streamsize i = 0L; i < sizeof(buffer); i++)
    {
        std::cout << buffer[i];
    }
    std::cout << std::endl;
    
    return std::string();
}