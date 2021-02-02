#!/bin/bash
java -cp "./libs/antlr-4.8-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -listener -visitor -o pddl/parser antlrHDDL.g4
