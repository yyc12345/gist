# Visual Studio Props File Writer

This is a small Python script which can write Visual Studio `.props` file.

Visual Studio `.props` file contains macro definations and else things. Programmer usually use it to define some maros pointing to dependencies, then they can refer these macros in project so the project self can be dependencies-independent. There is no need to modify project file self when migrating building environment. It is enough that just rewrite `.props` file and point macros to proper path inside it.

However, Visual Studio `.props` file is not a simple key-value file. So I create this script to help me write correct `.props` file.

Currently this script only support macro defination. It is vastly used by my projects.
