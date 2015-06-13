-- phpMyAdmin SQL Dump
-- version 4.3.9
-- http://www.phpmyadmin.net
--
-- 主機: localhost
-- 產生時間： 2015 年 06 月 12 日 16:19
-- 伺服器版本: 5.6.23
-- PHP 版本： 5.5.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 資料庫： `finance`
--

-- --------------------------------------------------------

--
-- 資料表結構 `DIVIDEND`
--

CREATE TABLE IF NOT EXISTS `DIVIDEND` (
  `INDEX` int(11) NOT NULL,
  `DATE` date NOT NULL,
  `PRICING` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 資料表結構 `DIVIDEND_ETF`
--

CREATE TABLE IF NOT EXISTS `DIVIDEND_ETF` (
  `INDEX` int(11) NOT NULL,
  `DATE` date NOT NULL,
  `PRICING` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 資料表結構 `SYMBOL`
--

CREATE TABLE IF NOT EXISTS `SYMBOL` (
  `INDEX` int(11) NOT NULL,
  `TICKER` text NOT NULL,
  `EXCHANGE` text NOT NULL,
  `NAME` text NOT NULL,
  `CATEGORY` text NOT NULL,
  `DIVIDEND` tinyint(1) NOT NULL DEFAULT '0',
  `DIVIDEND_TYPE` text NOT NULL,
  `DIVIDENDS_A_YEAR` int(11) NOT NULL DEFAULT '0',
  `YEARS` int(11) NOT NULL DEFAULT '0',
  `SOURCE` text,
  `PRICE` float NOT NULL DEFAULT '0',
  `RRI9` float NOT NULL DEFAULT '0',
  `RRI11` float NOT NULL DEFAULT '0',
  `RRI14` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 已匯出資料表的索引
--

--
-- 資料表索引 `SYMBOL`
--
ALTER TABLE `SYMBOL`
  ADD PRIMARY KEY (`INDEX`);

--
-- 在匯出的資料表使用 AUTO_INCREMENT
--

--
-- 使用資料表 AUTO_INCREMENT `SYMBOL`
--
ALTER TABLE `SYMBOL`
  MODIFY `INDEX` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
