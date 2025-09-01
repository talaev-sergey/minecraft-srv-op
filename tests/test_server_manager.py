# tests/test_server_manager.py

import pytest
import os
from server_manager import ServerManager
from server_status import ServerStatus

@pytest.fixture
def server_manager_instance(mocker):
    """
    Creates a ServerManager instance with mocked dependencies.
    """
    mock_alert_window = mocker.MagicMock()
    mock_update_callback = mocker.MagicMock()
    
    manager = ServerManager(
        rcon_host="localhost",
        rcon_password="password",
        rcon_port=25575,
        alert_window=mock_alert_window,
        update_status_callback=mock_update_callback
    )
    manager.alert_window = mock_alert_window
    manager.update_status_callback = mock_update_callback
    return manager

def test_start_server_linux_success(mocker, server_manager_instance):
    """
    Tests that start_server correctly calls subprocess.Popen on Linux.
    """
    def run_thread_target_synchronously(target=None, daemon=None):
        mock_instance = mocker.MagicMock()
        if target:
            mock_instance.start.side_effect = target
        return mock_instance

    mocker.patch('settings.Settings.get', return_value='/path/to/start.sh')
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('platform.system', return_value='Linux')
    mock_popen = mocker.patch('subprocess.Popen')
    mocker.patch('threading.Thread', side_effect=run_thread_target_synchronously)

    server_manager_instance.start_server()

    mock_popen.assert_called_once_with(
        ['bash', '/path/to/start.sh'],
        cwd='/path/to'
    )
    server_manager_instance.update_status_callback.assert_called_once()

def test_start_server_windows_success(mocker, server_manager_instance):
    """
    Tests that start_server correctly calls subprocess.Popen on Windows.
    This test uses a POSIX-style path to avoid issues with os.path on the host OS.
    """
    def run_thread_target_synchronously(target=None, daemon=None):
        mock_instance = mocker.MagicMock()
        if target:
            mock_instance.start.side_effect = target
        return mock_instance

    # Use a POSIX-style path; the logic only checks the .endswith(".bat") part.
    script_path = '/server/start.bat'
    mocker.patch('settings.Settings.get', return_value=script_path)
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('platform.system', return_value='Windows')
    mock_popen = mocker.patch('subprocess.Popen')
    mocker.patch('threading.Thread', side_effect=run_thread_target_synchronously)

    server_manager_instance.start_server()

    # The important part is that ["cmd.exe", "/c", ...] is called.
    mock_popen.assert_called_once_with(
        ['cmd.exe', '/c', script_path],
        cwd=os.path.dirname(script_path)
    )
    server_manager_instance.update_status_callback.assert_called_once()

def test_start_server_script_not_found(mocker, server_manager_instance):
    """
    Tests that an error is shown if the script file does not exist.
    """
    script_path = '/path/to/nonexistent.sh'
    mocker.patch('settings.Settings.get', return_value=script_path)
    mocker.patch('os.path.isfile', return_value=False)
    mock_popen = mocker.patch('subprocess.Popen')

    server_manager_instance.start_server()

    expected_error = f"Скрипт не найден:\n{script_path}"
    server_manager_instance.alert_window.set_error.assert_called_once_with(expected_error)
    mock_popen.assert_not_called()

def test_start_server_script_not_set(mocker, server_manager_instance):
    """
    Tests that an error is shown if the script is not set in settings.
    """
    mocker.patch('settings.Settings.get', return_value=None)
    mock_popen = mocker.patch('subprocess.Popen')

    server_manager_instance.start_server()

    server_manager_instance.alert_window.set_error.assert_called_once()
    mock_popen.assert_not_called()


def test_get_local_ip_success(mocker, server_manager_instance):
    """
    Tests that get_local_ip returns the correct IP on success.
    """
    # Mock socket.socket to avoid real network calls
    mock_socket = mocker.patch('server_manager.socket.socket').return_value
    
    # Configure the mock to return a fake IP
    fake_ip = '192.168.1.100'
    mock_socket.getsockname.return_value = [fake_ip]
    
    # Call the method
    ip = server_manager_instance.get_local_ip()
    
    # Assert that the correct IP is returned
    assert ip == fake_ip
    # Assert that the socket was correctly used
    mock_socket.connect.assert_called_once_with(('8.8.8.8', 80))
    mock_socket.close.assert_called_once()

def test_get_local_ip_failure(mocker, server_manager_instance):
    """
    Tests that get_local_ip returns '127.0.0.1' on failure
    and calls the alert window.
    """
    # Mock socket.socket to raise an exception
    mock_socket = mocker.patch('server_manager.socket.socket').return_value
    mock_socket.connect.side_effect = OSError("Test error")
    
    # Call the method
    ip = server_manager_instance.get_local_ip()
    
    # Assert that the fallback IP is returned
    assert ip == '127.0.0.1'
    
    # Assert that the error alert was triggered
    server_manager_instance.alert_window.set_error.assert_called_once()

@pytest.mark.parametrize(
    "port_65_open, port_75_open, rcon_ok, initial_status, expected_status",
    [
        # Server is fully online
        (True, True, True, ServerStatus.OFFLINE, ServerStatus.ONLINE),
        # Server is starting (main port open, but RCON not yet available)
        (True, True, False, ServerStatus.OFFLINE, ServerStatus.STARTING),
        # An unusual state where the RCON port is closed but the main one is open
        (True, False, True, ServerStatus.OFFLINE, ServerStatus.RCON_CLOSED),
        # Server is stopping (main port closed, RCON port still open)
        (False, True, False, ServerStatus.ONLINE, ServerStatus.STOPING),
        # Server is restarting (status should persist during this state)
        (False, True, False, ServerStatus.RESTATING, ServerStatus.RESTATING),
        # Server is fully offline
        (False, False, False, ServerStatus.ONLINE, ServerStatus.OFFLINE),
    ],
)
def test_update_server_status(
    mocker,
    port_65_open,
    port_75_open,
    rcon_ok,
    initial_status,
    expected_status,
):
    """
    Tests the update_server_status method across various scenarios
    by mocking the internal helper methods.
    """
    # --- Setup Mocks ---
    # Patch the internal helper methods directly
    def mock_check_port(port):
        if port == 25565:
            return port_65_open
        if port == 25575:
            return port_75_open
        return False

    mocker.patch(
        "server_manager.ServerManager._check_port",
        side_effect=mock_check_port
    )
    mocker.patch(
        "server_manager.ServerManager._rcon_is_ok",
        return_value=rcon_ok
    )

    # --- Create Instance ---
    mock_alert_window = mocker.MagicMock()
    mock_update_callback = mocker.MagicMock()
    manager = ServerManager(
        rcon_host="localhost",
        rcon_password="password",
        rcon_port=25575,
        alert_window=mock_alert_window,
        update_status_callback=mock_update_callback
    )
    manager.set_status(initial_status)

    # --- Execute ---
    manager.update_server_status()

    # --- Assert ---
    assert manager.get_status() == expected_status
    mock_update_callback.assert_called_once()
