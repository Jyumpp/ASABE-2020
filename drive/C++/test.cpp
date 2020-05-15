#include "LineCorrection/LineCorrection.h"
#include <stdio.h>
#include <unistd.h>

int main(){
  int anglePipe[2];
  int distancePipe[2];
  if(pipe(anglePipe) < 0){
    perror("pipe");
  }
  if(pipe(distancePipe) < 0){
    perror("pipe");
  }
  LineCorrection correction = LineCorrection(anglePipe[0],distancePipe[0],"test");
  return 0;
}
