#include "Menu.hpp"

func acpp::GetFunc(std::string func_name)
{
    std::map<std::string, func>::const_iterator funcdict_itr = (*func_dict).find(func_name);
    if (funcdict_itr == (*func_dict).end())
    {
        return &acpp::print_Func_not_found;
    }

    return funcdict_itr->second;
}

void acpp::initMap()
{
    func_dict = std::make_unique<std::map<std::string, func>>();
    (*func_dict)["--help"] = &print_help;

    // testing md5
 #ifdef DEBUGING_MODE_ON
    if (GetMD5String("Test") != "0cbc6611f5540bd0809a388dc95a615b")
    {
        throw std::string("Error md5 Failed");
    }
    std::cout << "Menu.cpp - Debug: Md5 Successed" << std::endl;
#endif
}

t_ReturnMessage acpp::print_help(std::vector<std::string> args)
{
    std::cout << "Options:"
              << "-n / --add-new <file_path> = add new file to the file codes to compile" << std::endl
              << "-c / --Compile = compiling all the files" << std::endl
              << "-o / --Compile-optimized = Compile all the files with optimize" << std::endl
              << "-s / --set-output-file <path>" << std::endl
              << "-l / --files-list = get header files list" << std::endl
              << std::endl
              << "compile options:" << std::endl
              << "-n / --no-linker = compile without using linker file compile all at once" << std::endl
              << "-f / --force = force compiling all the files" << std::endl
              << "-r / --rebuild-objects = rebuild all the objects" << std::endl
              << "can't use force compile and no-linker at the same time the no-linker will get canceled" << std::endl
              << std::endl
              << "add-new options:" << std::endl
              << "-a -auto-add-cpp = automaticly adding all the cpp files in the folders under the main one" << std::endl
              << std::endl
              << "files-list: " << std::endl
              << "showing you list of all the files that been added to the list of the files to compile" << std::endl;
    return 0;
}

t_ReturnMessage acpp::print_Func_not_found(std::vector<std::string> args)
{
    std::cerr << "Error: Unknown command " << std::endl;
    std::cout << "For options use flag --help" << std::endl;
    return 7;
}