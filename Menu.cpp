#include "Menu.hpp"

void acpp::print_help()
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
}