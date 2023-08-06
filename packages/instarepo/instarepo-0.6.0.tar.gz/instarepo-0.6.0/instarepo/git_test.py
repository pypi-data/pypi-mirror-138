from pytest_mock import MockerFixture
import instarepo.git


def test_clone(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")

    # act
    result = instarepo.git.clone("ssh://hello.git", "/tmp/hello")

    # assert
    mock.assert_called_once_with(
        ["git", "clone", "ssh://hello.git", "/tmp/hello"], check=True
    )
    assert result.dir == "/tmp/hello"


def test_clone_quietly(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")

    # act
    result = instarepo.git.clone("ssh://hello.git", "/tmp/hello", quiet=True)

    # assert
    mock.assert_called_once_with(
        ["git", "clone", "-q", "ssh://hello.git", "/tmp/hello"], check=True
    )
    assert result.dir == "/tmp/hello"


def test_create_branch(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello")

    # act
    git.create_branch("release")

    # assert
    mock.assert_called_once_with(
        ["git", "checkout", "-b", "release"], check=True, cwd="/tmp/hello"
    )


def test_create_branch_quietly(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello", quiet=True)

    # act
    git.create_branch("release")

    # assert
    mock.assert_called_once_with(
        ["git", "checkout", "-q", "-b", "release"], check=True, cwd="/tmp/hello"
    )


def test_add(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello")

    # act
    git.add("test.txt")

    # assert
    mock.assert_called_once_with(
        ["git", "add", "test.txt"], check=True, cwd="/tmp/hello"
    )


def test_commit(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello")

    # act
    git.commit("oops")

    # assert
    mock.assert_called_once_with(
        ["git", "commit", "-m", "oops"], check=True, cwd="/tmp/hello"
    )


def test_commit_quietly(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello", quiet=True)

    # act
    git.commit("oops")

    # assert
    mock.assert_called_once_with(
        ["git", "commit", "-q", "-m", "oops"], check=True, cwd="/tmp/hello"
    )


def test_push(mocker: MockerFixture):
    # arrange
    mock = mocker.patch("subprocess.run")
    git = instarepo.git.GitWorkingDir("/tmp/hello")

    # act
    git.push()

    # assert
    mock.assert_called_once_with(
        ["git", "push", "-u", "origin", "HEAD"], check=True, cwd="/tmp/hello"
    )


def test_join():
    git = instarepo.git.GitWorkingDir("/tmp/hello")
    filename = git.join("src", "index.js").replace("\\", "/")
    assert filename == "/tmp/hello/src/index.js"
