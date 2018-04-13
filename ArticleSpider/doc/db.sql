CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) DEFAULT NULL,
  `fav_nums` int(11) DEFAULT NULL,
  `praise_nums` int(11) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `zhihu_question` (
  `zhihu_id` bit(1) NOT NULL,
  `topics` varchar(255) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `answer_num` int(11) NOT NULL,
  `comments_num` int(11) NOT NULL,
  `watch_user_num` int(11) NOT NULL,
  `click_num` int(11) NOT NULL,
  `crawl_time` datetime NOT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `zhihu_answer` (
  `zhihu_id` bigint(20) NOT NULL,
  `url` varchar(300) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  `author_id` varchar(100) DEFAULT NULL,
  `content` longtext NOT NULL,
  `praise_num` int(11) NOT NULL,
  `comments_num` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime NOT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


