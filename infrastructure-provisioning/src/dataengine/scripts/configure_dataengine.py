#!/usr/bin/python

# *****************************************************************************
#
# Copyright (c) 2016, EPAM SYSTEMS INC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ******************************************************************************

import argparse
import json
import sys
from dlab.notebook_lib import *
from dlab.actions_lib import *
from dlab.fab import *
import os


parser = argparse.ArgumentParser()
parser.add_argument('--hostname', type=str, default='')
parser.add_argument('--keyfile', type=str, default='')
parser.add_argument('--region', type=str, default='')
parser.add_argument('--spark_version', type=str, default='')
parser.add_argument('--hadoop_version', type=str, default='')
parser.add_argument('--os_user', type=str, default='')
parser.add_argument('--scala_version', type=str, default='')
parser.add_argument('--r_mirror', type=str, default='')
parser.add_argument('--master_ip', type=str, default='')
parser.add_argument('--node_type', type=str, default='')
args = parser.parse_args()

spark_version = args.spark_version
hadoop_version = args.hadoop_version
tensorflow_version = os.environ['notebook_tensorflow_version']
nvidia_version = os.environ['notebook_nvidia_version']
theano_version = os.environ['notebook_theano_version']
keras_version = os.environ['notebook_keras_version']
caffe_version = os.environ['notebook_caffe_version']
caffe2_version = os.environ['notebook_caffe2_version']
cntk_version = os.environ['notebook_cntk_version']
mxnet_version = os.environ['notebook_mxnet_version']
python3_version = "3.4"
scala_link = "http://www.scala-lang.org/files/archive/"
if args.region == 'cn-north-1':
    spark_link = "http://mirrors.hust.edu.cn/apache/spark/spark-" + spark_version + "/spark-" + spark_version + \
                 "-bin-hadoop" + hadoop_version + ".tgz"
else:
    spark_link = "http://d3kbcqa49mib13.cloudfront.net/spark-" + spark_version + "-bin-hadoop" + hadoop_version + ".tgz"

templates_dir = '/root/templates/'
files_dir = '/root/files/'
local_spark_path = '/opt/spark/'
jars_dir = '/opt/jars/'
r_libs = ['R6', 'pbdZMQ', 'RCurl', 'devtools', 'reshape2', 'caTools', 'rJava', 'ggplot2']


def start_spark(os_user, master_ip, node):
    if not exists('/home/{0}/.ensure_dir/start_spark-{1}_ensured'.format(os_user, node)):
        run('mv /opt/spark/conf/spark-env.sh.template /opt/spark/conf/spark-env.sh')
        run('''echo "SPARK_MASTER_HOST='{}'" >> /opt/spark/conf/spark-env.sh'''.format(master_ip))
        if os.environ['application'] == 'tensor' or os.environ['application'] == 'deeplearning':
            run('''echo "LD_LIBRARY_PATH=/opt/cudnn/lib64:/usr/local/cuda/lib64" >> /opt/spark/conf/spark-env.sh''')
        if node == 'master':
            run('/opt/spark/sbin/start-master.sh')
            run('/opt/spark/sbin/start-slave.sh  spark://{}:7077'.format(master_ip))
        if node == 'slave':
            run('/opt/spark/sbin/start-slave.sh  spark://{}:7077'.format(master_ip))
        sudo('touch /home/{0}/.ensure_dir/start_spark-{1}_ensured'.format(os_user, node))


##############
# Run script #
##############
if __name__ == "__main__":
    print("Configure connections")
    env['connection_attempts'] = 100
    env.key_filename = [args.keyfile]
    env.host_string = args.os_user + '@' + args.hostname

    print("Configuring notebook server.")
    try:
        if not exists('/home/' + args.os_user + '/.ensure_dir'):
            sudo('mkdir /home/' + args.os_user + '/.ensure_dir')
    except:
        sys.exit(1)

    print("Install Java")
    ensure_jre_jdk(args.os_user)

    print("Install Spark")
    ensure_local_spark(args.os_user, spark_link, spark_version, hadoop_version, local_spark_path)

    print("Install jars for storage")
    ensure_local_jars(args.os_user, jars_dir, files_dir, args.region, templates_dir)

    print("Install Scala")
    ensure_scala(scala_link, args.scala_version, args.os_user)

    print("Install python2 libraries")
    ensure_python2_libraries(args.os_user)

    print("Install python3 libraries")
    ensure_python3_libraries(args.os_user)

    print("Installing R")
    ensure_r(args.os_user, r_libs, args.region, args.r_mirror)

    if os.environ['application'] in ('jupyter', 'zeppelin', 'tensor'):
        print("Installing opencv-python, h5py")
        ensure_additional_python_libs(args.os_user)

        print("Installing matplotlib.")
        ensure_matplot(args.os_user)

    if os.environ['application'] == 'jupyter':
        print("Installing notebook additions: sbt.")
        ensure_sbt(args.os_user)

        print("Installing Breeze library")
        add_breeze_library_local(args.os_user)

    if os.environ['application'] == 'zeppelin':
        print("Installing additional R packages")
        install_r_packages(args.os_user)

        print("Install python3 specific version")
        ensure_python3_specific_version(python3_version, args.os_user)

    if os.environ['application'] in ('tensor', 'deeplearning'):
        print("Installing TensorFlow")
        install_tensor(args.os_user, tensorflow_version, files_dir, templates_dir, nvidia_version)

        print("Install Theano")
        install_theano(args.os_user, theano_version)

        print("Installing Keras")
        install_keras(args.os_user, keras_version)

    if os.environ['application'] == 'deeplearning':
        print("Installing Caffe")
        install_caffe(args.os_user, args.region, caffe_version)

        print("Installing Caffe2")
        install_caffe2(args.os_user, caffe2_version)

        print("Installing Torch")
        install_torch(args.os_user)

        print("Install CNTK Python library")
        install_cntk(args.os_user, cntk_version)

        print("Installing MXNET")
        install_mxnet(args.os_user, mxnet_version)

    if args.node_type == 'master':
        print("Starting Spark master")
        start_spark(args.os_user, args.hostname, node='master')
    elif args.node_type == 'slave':
        print("Starting Spark slave")
        start_spark(args.os_user, args.master_ip, node='slave')
