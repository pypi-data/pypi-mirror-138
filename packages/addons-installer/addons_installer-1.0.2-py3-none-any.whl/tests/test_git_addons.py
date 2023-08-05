import os
import unittest
from typing import Dict, Callable

from addons_installer import (
    GitOdooAddons,
    KeySuffix,
    LocalOdooAddons,
    AddonsRegistry,
    LocalGitSubDirOdooAddons,
    OdooAddonsDef,
)


class TestGitAddonsSuffix(unittest.TestCase):
    def setUp(self) -> None:
        self.suffix = GitOdooAddons("MY_PROJECT")

    def test_name_suffix(self):
        self.assertEqual(9, len(self.suffix.get_suffix_keys()))
        self.assertEqual("ADDONS_GIT_MY_PROJECT_BRANCH", self.suffix.BRANCH.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_BRANCH", self.suffix.BRANCH.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_CLONE_PATH", self.suffix.CLONE_PATH.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_CLONE_PATH", self.suffix.CLONE_PATH.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_PULL_OPTIONS", self.suffix.PULL_OPTIONS.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_PULL_OPTIONS", self.suffix.PULL_OPTIONS.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_PROTOCOLE", self.suffix.PROTOCOLE.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_PROTOCOLE", self.suffix.PROTOCOLE.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN", self.suffix.HTTPS_LOGIN.full_key)
        self.assertIsNone(self.suffix.HTTPS_LOGIN.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD", self.suffix.HTTPS_PASSWORD.full_key)
        self.assertIsNone(self.suffix.HTTPS_PASSWORD.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_SSH_KEY", self.suffix.SSH_KEY.full_key)
        self.assertIsNone(self.suffix.SSH_KEY.default_key)
        self.assertEqual("ADDONS_GIT_MY_PROJECT_SERVER", self.suffix.SERVER.full_key)
        self.assertEqual("ADDONS_GIT_DEFAULT_SERVER", self.suffix.SERVER.default_key)

    def test_extract_raise_no_server(self):
        with self.assertRaises(ValueError) as e:
            self.suffix.extract({"ADDONS_GIT_MY_PROJECT_BRANCH": "branch_name"})
        self.assertEqual(
            "Not git server is provided, key [ADDONS_GIT_MY_PROJECT_SERVER] or [ADDONS_GIT_DEFAULT_SERVER]",
            e.exception.args[0],
        )

    def get_result(self, other_keys):
        # type: (Dict[str, str]) -> AddonsGitSuffix.Result
        return self.suffix.extract(
            {"ADDONS_GIT_MY_PROJECT": "my-project", "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com", **other_keys}
        )

    def test_extract_default_value(self):
        result = self.get_result({})
        self.assertEqual("gitlab.com", result.server)
        self.assertEqual("public", result.protocole)
        self.assertEqual("master", result.branch)
        self.assertEqual("/opt/addons/my-project", result.clone_path)
        self.assertIsNone(result.https_password)
        self.assertIsNone(result.https_login)
        self.assertEqual("https://%(server)s/%(git_path)s.git", result.format)
        self.assertIsNone(result.ssh_key)
        self.assertEqual("--depth=1 --quiet --single-branch", result.pull_options)

    def test_extract_BRANCH(self):
        self.factory_test_extract(self.suffix.BRANCH, "--value", lambda r: r.branch)

    def test_extract_CLONE_PATH(self):
        self.factory_test_extract(self.suffix.CLONE_PATH, "value", lambda r: r.clone_path)

        # Test expand user
        result = self.get_result({"ADDONS_GIT_MY_PROJECT_CLONE_PATH": "~/src"})
        self.assertEqual(os.path.expanduser("~/src"), result.clone_path)

    def test_extract_PULL_OPTIONS(self):
        self.factory_test_extract(self.suffix.PULL_OPTIONS, "value", lambda r: r.pull_options)

    def test_extract_PROTOCOLE_raise(self):
        value = "wrong_value"
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": value})
        self.assertEqual(
            "The selected protocole wrong_value is not supported, possible values are ['https', 'ssh', 'public']",
            e.exception.args[0],
        )

        # Test case sensitive
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "HTTPS"})
        self.assertEqual(
            "The selected protocole HTTPS is not supported, possible values are ['https', 'ssh', 'public']",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_HTTPS_missing_values(self):
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https"})
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )
        with self.assertRaises(ValueError) as e:
            self.get_result(
                {
                    "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                    "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                }
            )
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )
        with self.assertRaises(ValueError) as e:
            self.get_result(
                {
                    "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                    "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
                }
            )
        self.assertEqual(
            "Please add ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN and ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD var in your environment when you use [https] has git protocole",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_HTTPS(self):
        result = self.get_result(
            {
                "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "https",
                "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
            }
        )
        self.assertEqual(result.protocole, "https")
        self.assertEqual(result.https_login, "login")
        self.assertEqual(result.https_password, "password")
        self.assertIsNone(result.ssh_key)
        self.assertEqual(result.format, "https://%(login)s:%(password)s@%(server)s/%(git_path)s.git")
        self.assertEqual(result.git_url, "https://login:password@gitlab.com/my-project.git")

    def test_extract_PROTOCOLE_SSH(self):
        with self.assertRaises(ValueError) as e:
            self.get_result({"ADDONS_GIT_MY_PROJECT_PROTOCOLE": "ssh"})
        self.assertEqual(
            "Protocole [ssh] not supported for the moment",
            e.exception.args[0],
        )

    def test_extract_PROTOCOLE_PUBLIC(self):
        result = self.get_result(
            {
                "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
                # Fake key, test is removed after
                "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
                "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
                "ADDONS_GIT_MY_PROJECT_SSH_KEY": "my-key",
            }
        )
        self.assertEqual(result.protocole, "public")
        self.assertIsNone(result.https_login)
        self.assertIsNone(result.https_password)
        self.assertIsNone(result.ssh_key)
        self.assertEqual(result.format, "https://%(server)s/%(git_path)s.git")
        self.assertEqual(result.git_url, "https://gitlab.com/my-project.git")

    def test_extract_SERVER(self):
        self.factory_test_extract(self.suffix.SERVER, "server_git", lambda r: r.server)

    def factory_test_extract(self, suffix, value, getter):
        # type: (KeySuffix, str, Callable[[GitOdooAddons.Result], str]) -> None
        result = self.get_result({suffix.full_key: value})
        self.assertEqual(value, getter(result))

        result = self.get_result({suffix.default_key: value + "_1"})
        self.assertEqual(value + "_1", getter(result))
        result = self.get_result(
            {
                suffix.full_key: value + "_3",
                suffix.default_key: value + "_2",
            }
        )
        self.assertEqual(value + "_3", getter(result))


class TestLocalAddonsSuffix(unittest.TestCase):
    def setUp(self):
        self.suffix = LocalOdooAddons("ADDONS_LOCAL_MY_PROJECT")

    def test_local(self):
        self.assertEqual("MY_PROJECT", self.suffix.identifier)
        self.assertTrue(self.suffix.is_valid())
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", self.suffix.NAME.full_key)
        self.assertIsNone(self.suffix.NAME.default_key)

        self.assertEqual("ADDONS_LOCAL_MY_PROJECT_BASE_PATH", self.suffix.BASE_PATH.full_key)
        self.assertEqual("ADDONS_LOCAL_DEFAULT_BASE_PATH", self.suffix.BASE_PATH.default_key)


class TestAddonsRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = AddonsRegistry()

    def test_parse_key_local(self):
        res = self.registry.parse_key("ADDONS_LOCAL_MY_PROJECT")
        self.assertIsNotNone(res)
        self.assertEqual(type(res), LocalOdooAddons)
        self.assertEqual("ADDONS_LOCAL_MY_PROJECT", res.base_key)
        self.assertEqual("MY_PROJECT", res.identifier)
        self.assertEqual("ADDONS_LOCAL", res.prefix)

    def test_parse_key_git(self):
        res = self.registry.parse_key("ADDONS_GIT_MY_PROJECT")
        self.assertIsNotNone(res)
        self.assertEqual(type(res), GitOdooAddons)
        self.assertEqual("ADDONS_GIT_MY_PROJECT", res.base_key)
        self.assertEqual("MY_PROJECT", res.identifier)
        self.assertEqual("ADDONS_GIT", res.prefix)

    def test_parse_key_none(self):
        res = self.registry.parse_key("ADDONS_MY_PROJECT")
        self.assertIsNone(res)

    def test_parse_env_empty(self):
        """No default value returned"""
        addons_definitions = self.registry.parse_env({})
        self.assertFalse(addons_definitions)

    def test_parse_env_odoo_path(self):
        addons_definitions = self.registry.parse_env({"ODOO_PATH": "/odoo"})
        self.assertEqual(2, len(addons_definitions))
        names = {"ADDONS_LOCAL_SRC_ODOO_ADDONS", "ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS"}
        self.assertEqual(names, set(map(lambda it: it.name, addons_definitions)))
        # order is not valid in set, so we do a swap if needed.
        base_addon, addons = addons_definitions
        if base_addon.name == "ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS":
            addons, base_addon = addons_definitions

        self.assertEqual("ADDONS_LOCAL_SRC_ODOO_ADDONS_ADDONS", addons.name)
        self.assertEqual("ADDONS_LOCAL_SRC_ODOO_ADDONS", base_addon.name)
        self.assertEqual(type(base_addon), LocalOdooAddons.Result)
        self.assertEqual(type(addons), LocalOdooAddons.Result)
        self.assertEqual("/odoo/odoo/addons", addons.addons_path)
        self.assertEqual("/odoo/addons", base_addon.addons_path)
        self.assertEqual([], base_addon.install_cmd())
        self.assertEqual([], addons.install_cmd())

    def test_parse_env_git_public(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
            # Fake key, test is removed after
            # "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
            # "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
            # "ADDONS_GIT_MY_PROJECT_SSH_KEY": "my-key",
        }
        results = self.registry.parse_env(env_vars)
        self.assertEqual(1, len(results))
        result = results.pop()
        self.assertIsInstance(result, GitOdooAddons.Result)
        self.assertEqual("my-project", result.git_path)
        self.assertEqual("master", result.branch)
        self.assertEqual("/opt/addons/my-project", result.clone_path)
        self.assertEqual("--depth=1 --quiet --single-branch", result.pull_options)
        self.assertIsNone(result.https_login)
        self.assertIsNone(result.https_password)
        self.assertIsNone(result.ssh_key)
        self.assertEqual("public", result.protocole)
        self.assertEqual("gitlab.com", result.server)
        self.assertEqual("https://%(server)s/%(git_path)s.git", result.format)
        self.assertEqual("https://gitlab.com/my-project.git", result.git_url)
        install_cmds = result.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertEqual(7, len(install_cmd))
        self.assertEqual(
            [
                "git",
                "clone",
                "--depth=1 --quiet --single-branch",
                "-b",
                "master",
                "https://gitlab.com/my-project.git",
                "/opt/addons/my-project",
            ],
            install_cmd,
        )

    def test_parse_env_git_https(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            # Fake key, test is removed after
            "ADDONS_GIT_MY_PROJECT_HTTPS_LOGIN": "login",
            "ADDONS_GIT_MY_PROJECT_HTTPS_PASSWORD": "password",
        }
        results = self.registry.parse_env(env_vars)
        self.assertEqual(1, len(results))
        result = results.pop()
        self.assertIsInstance(result, GitOdooAddons.Result)
        self.assertEqual("my-project", result.git_path)
        self.assertEqual("master", result.branch)
        self.assertEqual("/opt/addons/my-project", result.clone_path)
        self.assertEqual("--depth=1 --quiet --single-branch", result.pull_options)
        self.assertEqual("https", result.protocole)
        self.assertEqual("login", result.https_login)
        self.assertEqual("password", result.https_password)
        self.assertIsNone(result.ssh_key)
        self.assertEqual("gitlab.com", result.server)
        self.assertEqual("https://%(login)s:%(password)s@%(server)s/%(git_path)s.git", result.format)
        self.assertEqual("https://login:password@gitlab.com/my-project.git", result.git_url)
        install_cmds = result.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertEqual(7, len(install_cmd))
        self.assertEqual(
            [
                "git",
                "clone",
                "--depth=1 --quiet --single-branch",
                "-b",
                "master",
                "https://login:password@gitlab.com/my-project.git",
                "/opt/addons/my-project",
            ],
            install_cmd,
        )

    def test_parse_env_git_subdir(self):
        env_vars = {
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.com",
            "ADDONS_GIT_MY_PROJECT": "my-project",
            "ADDONS_GIT_MY_PROJECT_CLONE_PATH": "/src/path",
            "ADDONS_GIT_MY_PROJECT_PROTOCOLE": "public",
            # Key to test
            "ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT": "common",
        }
        results = self.registry.parse_env(env_vars)
        self.assertEqual(2, len(results))
        git_addon, sub_addon = results
        self.assertIsInstance(git_addon, OdooAddonsDef)
        self.assertIsInstance(sub_addon, OdooAddonsDef)
        if git_addon.name == "ADDONS_SUBDIR_GIT_COMMON_OF_MY_PROJECT":
            sub_addon, git_addon = results

        self.assertIsInstance(git_addon, GitOdooAddons.Result)
        self.assertEqual("my-project", git_addon.git_path)
        self.assertEqual("master", git_addon.branch)
        self.assertEqual("/src/path", git_addon.clone_path)
        self.assertEqual("--depth=1 --quiet --single-branch", git_addon.pull_options)
        self.assertIsNone(git_addon.https_login)
        self.assertIsNone(git_addon.https_password)
        self.assertIsNone(git_addon.ssh_key)
        self.assertEqual("public", git_addon.protocole)
        self.assertEqual("gitlab.com", git_addon.server)
        self.assertEqual("https://%(server)s/%(git_path)s.git", git_addon.format)
        self.assertEqual("https://gitlab.com/my-project.git", git_addon.git_url)
        install_cmds = git_addon.install_cmd()
        self.assertEqual(1, len(install_cmds))
        install_cmd = install_cmds[0]
        self.assertEqual(7, len(install_cmd))
        self.assertEqual(
            [
                "git",
                "clone",
                "--depth=1 --quiet --single-branch",
                "-b",
                "master",
                "https://gitlab.com/my-project.git",
                "/src/path",
            ],
            install_cmd,
        )

        self.assertIsInstance(sub_addon, LocalGitSubDirOdooAddons.Result)
        self.assertEqual("/src/path/common", sub_addon.full_path)
