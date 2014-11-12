SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

INSERT INTO `services` (`id`, `teamId`, `address`, `type`) VALUES
  (21, 1, '10.10.10.10', 'http'),
  (22, 1, 'google.com', 'http'),
  (23, 1, '10.10.10.10', 'https'),
  (24, 1, 'google.com', 'https'),
  (25, 1, '10.10.10.10', 'ftp'),
  (26, 1, 'ftp.swfwmd.state.fl.us', 'ftp'),
  (27, 1, '10.10.10.10', 'ssh'),
  (28, 1, 'jeffandolora.com', 'ssh'),
  (29, 1, '10.10.10.10', 'icmp'),
  (30, 1, 'google.com', 'icmp'),
  (31, 1, '10.10.10.10', 'smtp'),
  (32, 1, 'test.smtp.org', 'smtp'),
  (33, 1, '10.10.10.10', 'dns'),
  (34, 1, '8.8.8.8', 'dns');
