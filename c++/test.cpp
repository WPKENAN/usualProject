#include 'mpi.h'
#include <iostream>
 
int main(int argc,  char* argv[])
{
	int rank;
	int size;
	MPI\_Init(0,0);
	MPI\_Comm\_rank(MPI\_COMM\_WORLD, &rank);
	MPI\_Comm\_size(MPI\_COMM\_WORLD, &size);
	
	std::cout<<'Hello world from process '<<rank<<' of '<<size<<std::endl;
 
	MPI\_Finalize();
 
	return 0;
}