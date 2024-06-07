-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2024 at 10:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `belaz_gael_deva1a_suivi_notes`;

-- Use the database
USE `belaz_gael_deva1a_suivi_notes`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `belaz_gael_deva1a_suivi_notes`
--

-- --------------------------------------------------------

--
-- Table structure for table `t_apprenti`
--

CREATE TABLE `t_apprenti` (
  `id_apprennti` int(11) NOT NULL,
  `nom_apprenti` char(50) DEFAULT NULL,
  `prenom_apprenti` char(50) DEFAULT NULL,
  `filiere_apprenti` char(50) DEFAULT NULL,
  `ordonance_apprenti` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_apprenti`
--

INSERT INTO `t_apprenti` (`id_apprennti`, `nom_apprenti`, `prenom_apprenti`, `filiere_apprenti`, `ordonance_apprenti`) VALUES
(3, 'Belaz', 'Gael', 'Developpement', 2021),
(4, 'Nava', 'Justin', 'Operateur', 2018),
(5, 'Moore', 'William', 'Exploitation', 2021),
(6, 'Angelo', 'Mary', 'Developpement', 2017),
(7, 'Freed', 'Diane', 'Operateur', 2017);

-- --------------------------------------------------------

--
-- Table structure for table `t_matiere`
--

CREATE TABLE `t_matiere` (
  `id_matiere` int(11) NOT NULL,
  `nom_matiere` char(50) DEFAULT NULL,
  `fk_type_matiere` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_matiere`
--

INSERT INTO `t_matiere` (`id_matiere`, `nom_matiere`, `fk_type_matiere`) VALUES
(1, 'Math', 3),
(2, 'Anglais', 3),
(3, 'CultureGeneral', 3),
(4, 'i164', 1),
(5, 'i319', 1),
(6, 'i117', 2);

-- --------------------------------------------------------

--
-- Table structure for table `t_notes`
--

CREATE TABLE `t_notes` (
  `id_notes` int(11) NOT NULL,
  `notes` decimal(20,6) DEFAULT NULL,
  `fk_matiere` int(11) DEFAULT NULL,
  `fk_typeNotes` int(11) DEFAULT NULL,
  `fk_apprenti` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_notes`
--

INSERT INTO `t_notes` (`id_notes`, `notes`, `fk_matiere`, `fk_typeNotes`, `fk_apprenti`) VALUES
(1, 5.000000, 4, 1, 5),
(2, 4.000000, 1, 4, 6),
(3, 3.500000, 3, 3, 5),
(4, 6.000000, 4, 2, 3),
(5, 5.500000, 1, 4, 4),
(6, 2.000000, 2, 2, 5),
(7, 4.500000, 5, 1, 7);

-- --------------------------------------------------------

--
-- Table structure for table `t_suivi`
--

CREATE TABLE `t_suivi` (
  `id_suivi` int(11) NOT NULL,
  `fk_apprenti` int(11) DEFAULT NULL,
  `fk_matiere` int(11) DEFAULT NULL,
  `annee` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_suivi`
--

INSERT INTO `t_suivi` (`id_suivi`, `fk_apprenti`, `fk_matiere`, `annee`) VALUES
(1, 7, 4, 'Premiere'),
(2, 6, 5, 'Quatrieme'),
(3, 4, 2, 'Deuxieme'),
(4, 4, 4, 'Premiere'),
(5, 3, 1, 'Troisieme'),
(6, 7, 5, 'Quatrieme'),
(7, 5, 2, 'Troisieme');

-- --------------------------------------------------------

--
-- Table structure for table `t_type_matiere`
--

CREATE TABLE `t_type_matiere` (
  `id_type_matiere` int(11) NOT NULL,
  `type_matiere` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_type_matiere`
--

INSERT INTO `t_type_matiere` (`id_type_matiere`, `type_matiere`) VALUES
(1, 'ModuleEpsic'),
(2, 'ModuleCie'),
(3, 'BrancheGeneral');

-- --------------------------------------------------------

--
-- Table structure for table `t_type_notes`
--

CREATE TABLE `t_type_notes` (
  `id_type_notes` int(11) NOT NULL,
  `type_notes` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `t_type_notes`
--

INSERT INTO `t_type_notes` (`id_type_notes`, `type_notes`) VALUES
(1, 'Normal'),
(2, 'MoyenneSemestrielle'),
(3, 'MoyenneAnnuel'),
(4, 'MoyenneFinale');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `t_apprenti`
--
ALTER TABLE `t_apprenti`
  ADD PRIMARY KEY (`id_apprennti`);

--
-- Indexes for table `t_matiere`
--
ALTER TABLE `t_matiere`
  ADD PRIMARY KEY (`id_matiere`),
  ADD KEY `FK_matiere_type_matiere` (`fk_type_matiere`);

--
-- Indexes for table `t_notes`
--
ALTER TABLE `t_notes`
  ADD PRIMARY KEY (`id_notes`),
  ADD KEY `FK_notes_matiere` (`fk_matiere`),
  ADD KEY `FK_notes_type_notes` (`fk_typeNotes`),
  ADD KEY `FK_notes_apprenti` (`fk_apprenti`);

--
-- Indexes for table `t_suivi`
--
ALTER TABLE `t_suivi`
  ADD PRIMARY KEY (`id_suivi`),
  ADD KEY `FK__apprenti` (`fk_apprenti`),
  ADD KEY `FK_t_apprenti_matiere_matiere` (`fk_matiere`);

--
-- Indexes for table `t_type_matiere`
--
ALTER TABLE `t_type_matiere`
  ADD PRIMARY KEY (`id_type_matiere`);

--
-- Indexes for table `t_type_notes`
--
ALTER TABLE `t_type_notes`
  ADD PRIMARY KEY (`id_type_notes`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `t_apprenti`
--
ALTER TABLE `t_apprenti`
  MODIFY `id_apprennti` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `t_matiere`
--
ALTER TABLE `t_matiere`
  MODIFY `id_matiere` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `t_notes`
--
ALTER TABLE `t_notes`
  MODIFY `id_notes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `t_suivi`
--
ALTER TABLE `t_suivi`
  MODIFY `id_suivi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `t_type_matiere`
--
ALTER TABLE `t_type_matiere`
  MODIFY `id_type_matiere` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `t_type_notes`
--
ALTER TABLE `t_type_notes`
  MODIFY `id_type_notes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `t_matiere`
--
ALTER TABLE `t_matiere`
  ADD CONSTRAINT `FK_matiere_type_matiere` FOREIGN KEY (`fk_type_matiere`) REFERENCES `t_type_matiere` (`id_type_matiere`);

--
-- Constraints for table `t_notes`
--
ALTER TABLE `t_notes`
  ADD CONSTRAINT `FK_notes_apprenti` FOREIGN KEY (`fk_apprenti`) REFERENCES `t_apprenti` (`id_apprennti`),
  ADD CONSTRAINT `FK_notes_matiere` FOREIGN KEY (`fk_matiere`) REFERENCES `t_matiere` (`id_matiere`),
  ADD CONSTRAINT `FK_notes_type_notes` FOREIGN KEY (`fk_typeNotes`) REFERENCES `t_type_notes` (`id_type_notes`);

--
-- Constraints for table `t_suivi`
--
ALTER TABLE `t_suivi`
  ADD CONSTRAINT `FK__apprenti` FOREIGN KEY (`fk_apprenti`) REFERENCES `t_apprenti` (`id_apprennti`),
  ADD CONSTRAINT `FK_t_apprenti_matiere_matiere` FOREIGN KEY (`fk_matiere`) REFERENCES `t_matiere` (`id_matiere`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
