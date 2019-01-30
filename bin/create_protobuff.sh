#!/bin/bash

protoc -I=../Common/Network/Protobuff/ --python_out=../Common/Network/Protobuff/Generated/ ../Common/Network/Protobuff/packet.proto
