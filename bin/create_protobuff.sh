#!/bin/bash

protoc -I=../common/network/Protobuff/ --python_out=../common/network/Protobuff/Generated/ ../common/network/Protobuff/packet.proto
