import unittest
from unittest.mock import patch, MagicMock
from Robot.remote_control import RobotRemoteControl

class TestRobotRemoteControl(unittest.TestCase):
    def setUp(self):
        self.remote = RobotRemoteControl()
        self.remote._send_c_command = MagicMock(return_value=True)

    def test_forward_command(self):
        self.remote.do_forward("4 5")
        self.remote._send_c_command.assert_called_with("forward(4, 5);")

    def test_back_command(self):
        self.remote.do_back("3 2")
        self.remote._send_c_command.assert_called_with("back(3, 2);")

    def test_left_command(self):
        self.remote.do_left("90")
        self.remote._send_c_command.assert_called_with("turn_left(90);")

    def test_right_command(self):
        self.remote.do_right("45")
        self.remote._send_c_command.assert_called_with("turn_right(45);")

    def test_say_command(self):
        self.remote.do_say("你好")
        self.remote._send_c_command.assert_called_with('gpp_say(1, "你好");')

    def test_beep_command(self):
        self.remote.do_beep("440 1000")
        self.remote._send_c_command.assert_called_with("beep(440, 1000);")

    def test_exec_square(self):
        self.remote.do_exec("square")
        self.remote._send_c_command.assert_called()

    def test_exec_custom_code(self):
        test_code = "forward(4,5); turn_left(90);"
        self.remote.do_exec(test_code)
        self.remote._send_c_command.assert_called_with(test_code)

    @patch('requests.post')
    def test_send_c_command_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        remote = RobotRemoteControl()
        result = remote._send_c_command("test")
        self.assertTrue(result)

    @patch('requests.post')
    def test_send_c_command_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error"
        mock_post.return_value = mock_response
        
        remote = RobotRemoteControl()
        result = remote._send_c_command("test")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
