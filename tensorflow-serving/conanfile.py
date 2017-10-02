from conans import ConanFile, tools
import sys


class TensorflowservingConan(ConanFile):
    name = "TensorflowServing"
    version = "1.3.0_master"
    tag = "6330edb4bb7002b3bf8d32860c2e7fb0d5ab0a16"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone --recurse-submodules --depth 1 https://github.com/tensorflow/serving")
        self.run("cd serving && git checkout %s" % self.tag)

    def build(self):
        env = {
            "PYTHON_BIN_PATH": sys.executable,
            "USE_DEFAULT_PYTHON_LIB_PATH": "1",
            "CC_OPT_FLAGS": "-march=native",
            "TF_NEED_MKL": "0",
            "TF_NEED_GCP": "0",
            "TF_NEED_HDFS": "0",
            "TF_ENABLE_XLA": "0",
            "TF_NEED_VERBS": "0",
            "TF_NEED_OPENCL": "0",
            "TF_NEED_CUDA": "0",
            "TF_NEED_MPI": "0",
            "TF_NEED_GDR": "0",
            "TF_NEED_JEMALLOC": "1",
        }
        with tools.environment_append(env):
            self.output.info("Build environment: %s" % env)
            self.run("cd serving/tensorflow && ./configure")
            self.run("cd serving/ && bazel build -c opt tensorflow_serving/...")
            self.run("cd serving/ && ls -R")

    def package(self):
        self.copy("*.h", dst="include", src="./serving/tensorflow")
        self.copy("*.h", dst="include", src="./serving/tf_models/syntaxnet/tensorflow")
        self.copy("*.dll", dst="bin", src="serving/bazel-bin", keep_path=False)
        self.copy("*.so", dst="lib", src="serving/bazel-bin", keep_path=False)
        self.copy("*.dylib", dst="lib", src="serving/bazel-bin", keep_path=False)
        self.copy("*.a", dst="lib", src="serving/bazel-bin", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
