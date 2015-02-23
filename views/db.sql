-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Dec 04, 2014 at 03:07 AM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `employee_network`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_post`(post_id INT)
BEGIN
	delete from likes_post where post_id = post_id;
    delete from likes_comments where comment_id in (select comment_id from comments where post_id = post_id);
    delete from comments where post_id = post_id;
    delete from location_post where post_id = post_id;
    delete from user_post where post_id = post_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_post_1`(post_id INT)
BEGIN
	delete from likes_post where post_id = post_id;
    delete from likes_comment where comment_id in (select comment_id from comments where post_id = post_id);
    delete from comments where post_id = post_id;
    delete from location_post where post_id = post_id;
    delete from user_post where post_id = post_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `request_response`(from_user_id INT, to_user_id INT, response_code BINARY)
BEGIN
	if response_code then
    	insert into friends(user_id, friend_id) values(from_user_id, to_user_id);
    end if;
	delete from friend_requests where from_id = from_user_id and to_id = to_user_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE IF NOT EXISTS `comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `commented_when` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `friends`
--

CREATE TABLE IF NOT EXISTS `friends` (
  `user_id` int(11) NOT NULL,
  `friend_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`friend_id`),
  KEY `user_id` (`user_id`),
  KEY `friend_id` (`friend_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `friend_requests`
--

CREATE TABLE IF NOT EXISTS `friend_requests` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `from_id` int(11) NOT NULL,
  `to_id` int(11) NOT NULL,
  `when_sent` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  KEY `from_id` (`from_id`),
  KEY `to_id` (`to_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `likes_comment`
--

CREATE TABLE IF NOT EXISTS `likes_comment` (
  `comment_id` int(11) NOT NULL,
  `liked_by_id` int(11) NOT NULL,
  PRIMARY KEY (`comment_id`,`liked_by_id`),
  KEY `liked_by_id` (`liked_by_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `likes_post`
--

CREATE TABLE IF NOT EXISTS `likes_post` (
  `post_id` int(11) NOT NULL,
  `liked_by_id` int(11) NOT NULL,
  PRIMARY KEY (`post_id`,`liked_by_id`),
  KEY `likes_post_ibfk_2` (`liked_by_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_post`
--

CREATE TABLE IF NOT EXISTS `location_post` (
  `post_id` int(11) NOT NULL,
  `location_area` varchar(256) NOT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE IF NOT EXISTS `profile` (
  `user_id` int(11) NOT NULL,
  `school` varchar(256) NOT NULL,
  `university` varchar(256) NOT NULL,
  `job` varchar(256) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `relationship`
--

CREATE TABLE IF NOT EXISTS `relationship` (
  `relationship_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_id_map` int(11) NOT NULL,
  `relationship` varchar(60) NOT NULL,
  PRIMARY KEY (`relationship_id`),
  KEY `user_id` (`user_id`),
  KEY `user_id_map` (`user_id_map`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(256) NOT NULL,
  `first_name` varchar(256) NOT NULL,
  `last_name` varchar(256) NOT NULL,
  `email_id` varchar(256) NOT NULL,
  `join_date` date NOT NULL,
  `current_location` varchar(256) NOT NULL,
  `relationship_status` tinyint(1) NOT NULL,
  `date_of_birth` date NOT NULL,
  `profile_pic` blob NOT NULL,
  `friends_visibility_id` int(11) NOT NULL,
  `post_visibility_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `user_post`
--

CREATE TABLE IF NOT EXISTS `user_post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `posted_when` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1000) NOT NULL,
  `title` varchar(256) NOT NULL,
  `upload` varchar(100) NOT NULL,
  `visibility_id` int(11) NOT NULL DEFAULT '2',
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`),
  FULLTEXT KEY `content` (`content`,`title`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `user_post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `friends`
--
ALTER TABLE `friends`
  ADD CONSTRAINT `friends_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `friends_ibfk_2` FOREIGN KEY (`friend_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `friend_requests`
--
ALTER TABLE `friend_requests`
  ADD CONSTRAINT `friend_requests_ibfk_1` FOREIGN KEY (`from_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `friend_requests_ibfk_2` FOREIGN KEY (`to_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `likes_comment`
--
ALTER TABLE `likes_comment`
  ADD CONSTRAINT `likes_comment_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `likes_comment_ibfk_2` FOREIGN KEY (`liked_by_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `likes_post`
--
ALTER TABLE `likes_post`
  ADD CONSTRAINT `likes_post_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `user_post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `likes_post_ibfk_2` FOREIGN KEY (`liked_by_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `location_post`
--
ALTER TABLE `location_post`
  ADD CONSTRAINT `location_post_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `user_post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `profile`
--
ALTER TABLE `profile`
  ADD CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `relationship`
--
ALTER TABLE `relationship`
  ADD CONSTRAINT `relationship_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `relationship_ibfk_2` FOREIGN KEY (`user_id_map`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `user_post`
--
ALTER TABLE `user_post`
  ADD CONSTRAINT `user_post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
