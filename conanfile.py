from conans import ConanFile, CMake

class Jinja2CppConan(ConanFile):
    name = "Jinja2Cpp"
    version = "0.9.0"
    license = "Mozilla Public License Version 2.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    description = "Almost full-conformance template engine implementation"
    author = "Karl Wallner <kwallner@mail.de>"
    url = 'git@github.com:kwallner/Jinja2Cpp.git'
    scm = { "type": "git", "url": "auto", "revision": "auto" }
    no_copy_source = True

    def requirements(self):
        self.requires("boost/1.68.0@%s/%s" % ("kwallner", "testing"))
        self.requires("expected_lite/0.9.0@%s/%s" % ("kwallner", "testing"))
        self.requires("variant_lite/1.0.0@%s/%s" % ("kwallner", "testing"))
        self.requires("value_ptr_lite/0.0.0@%s/%s" % ("kwallner", "testing"))
        self.requires("optional_lite/3.1.1@%s/%s" % ("kwallner", "testing"))
       
    def build_requirements(self):
        self.build_requires("gtest/1.8.0@%s/%s" % ("kwallner", "testing"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["JINJA2CPP_BUILD_TESTS"] = True
        cmake.configure()
        cmake.build()
        cmake.install()
        cmake.test()
        
    def package_info(self):
        self.env_info.Jinja2Cpp_DIR = self.package_folder