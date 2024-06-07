/*Vous trouverez ci-dessous toute les requêtes utilisée dans les fichiers CRUD du projet*/

    /*Dossier "genres" | Contient les requêtes de la table apprenti*/
        /*genres_afficher*/
            /*Sélection de tout les apprentis*/
            SELECT * from t_apprenti

            /*Sélection d'un apprenti (Dans ce cas celui ayant l'id 4)*/
            SELECT * FROM t_apprenti WHERE id_apprennti = 1

            /*Sélectionne tout les apprentis avec les id dans un ordre décroissant*/
            SELECT * FROM t_apprenti ORDER BY id_apprennti DESC

        /*genres_ajouter*/
            /*Insertion d'un nouvel apprenti*/
            INSERT INTO t_apprenti (id_apprennti, nom_apprenti, prenom_apprenti, filiere_apprenti, ordonance_apprenti)  VALUES (NULL, 'Maccaud', 'Olivier', 'Developpement', 2021)

        /*genre_update*/
            /*Update un apprenti*/
            UPDATE t_apprenti 
                SET nom_apprenti = 'Paul', 
                    prenom_apprenti = 'Jean', 
                    filiere_apprenti = 'Operateur', 
                    ordonance_apprenti = 2020
                WHERE id_apprennti = 6

            /*Sélectionne les données voulues de l'apprenti*/
             SELECT id_apprennti, nom_apprenti, prenom_apprenti, filiere_apprenti, ordonance_apprenti 
                FROM t_apprenti 
                WHERE id_apprennti = 6

            /*Genre delete*/
                /*Supprime un apprenti*/
                DELETE FROM t_apprenti WHERE id_apprennti = 22

                /*Sélectionne l'apprenti à supprimer*/
                SELECT id_apprennti, nom_apprenti, prenom_apprenti, filiere_apprenti, ordonance_apprenti FROM t_apprenti WHERE id_apprennti = 22

            
            /*Dossier matiere*/
                /*Matiere_afficher*/
                    /*Affiche les données choisie*/
                    SELECT t_matiere.id_matiere, t_matiere.nom_matiere, t_type_matiere.type_matiere AS fk_type_matiere
                                                    FROM t_matiere
                                                    JOIN t_type_matiere ON t_matiere.fk_type_matiere = t_type_matiere.id_type_matiere; 

                    /*Sélectionne toute les données de la table matière en fonction de l'id*/
                    SELECT * FROM t_matiere WHERE id_matiere = 1
                
                /*matiere_ajouter*/
                    /*Insertion d'une nouvelle matière*/
                    INSERT INTO t_matiere (id_matiere, nom_matiere, fk_type_matiere) 
                         VALUES (NULL, '165', '1')

                /*matiere_update*/
                    /*Update une matière*/
                        UPDATE t_matiere
                        SET nom_matiere = 163,
                        fk_type_matiere = 2
                        WHERE id_matiere = 1
                
                    /*Sélectionne toute les données de la table matière*/
                    SELECT *
                    FROM t_matiere
                    WHERE id_matiere = 1


                /*Matiere_delete*/
                    /*Supprime une matière*/
                    DELETE FROM t_matiere WHERE id_matiere = 1

                    /*Sélectionne les données de la table matière*/ 
                        SELECT t_matiere.id_matiere, t_matiere.nom_matiere, t_type_matiere.type_matiere AS fk_type_matiere
                                                    FROM t_matiere
                                                    JOIN t_type_matiere ON t_matiere.fk_type_matiere = t_type_matiere.id_type_matiere;

                
            /*Dossier notes*/
                /*notes afficher*/
                    /*sélectionne toute les données de la table notes*/
                        SELECT tn.id_notes, tn.notes, tm.nom_matiere, ttn.type_notes, ta.nom_apprenti
                                                    FROM t_notes tn
                                                    INNER JOIN t_matiere tm ON tn.fk_matiere = tm.id_matiere
                                                    INNER JOIN t_type_notes ttn ON tn.fk_typeNotes = ttn.id_type_notes
                                                    INNER JOIN t_apprenti ta ON tn.fk_apprenti = ta.id_apprennti;

                    /*sélectionne toute les données de la table notes avec l'id spécifier*/
                        SELECT * FROM t_notes WHERE id_notes = 1

                    /*sélectionne toute les données de la table notes avec l'ordre des id en décroissant*/
                        SELECT * FROM t_notes ORDER BY id_notes DESC

                /*notes ajouter*/
                    /*Insert une nouvelle notes*/
                        INSERT INTO t_notes (id_notes, notes, fk_matiere, fk_typeNotes, fk_apprenti) 
                         VALUES (NULL, 5, 1, 1, 7)

                /*notes update*/
                    /*update une notes*/
                        UPDATE t_notes
                         SET notes = 4,
                            fk_apprenti = 6, 
                            fk_matiere = 3, 
                            fk_typeNotes = 3
                         WHERE id_notes = 6
                    /*récupére les champs à Update*/
                        SELECT *
                        FROM t_notes
                        WHERE id_notes = 6

                /*notes delete*/
                    /*Delete l'id sélectionner*/ 
                    DELETE FROM t_notes WHERE id_notes = 6

                    /*récupére les données qui vont être effacée*/
                    SELECT tn.id_notes, tn.notes, tm.nom_matiere, ttn.type_notes, ta.nom_apprenti
                                                    FROM t_notes tn
                                                    INNER JOIN t_matiere tm ON tn.fk_matiere = tm.id_matiere
                                                    INNER JOIN t_type_notes ttn ON tn.fk_typeNotes = ttn.id_type_notes
                                                    INNER JOIN t_apprenti ta ON tn.fk_apprenti = ta.id_apprennti
                                                     WHERE id_notes = 6

            /*dossier type matiere*/
                /*afficher*/
                    /*sélectionne le type de matière*/
                        SELECT * FROM t_type_matiere WHERE id_type_matiere = 1
                    /*Sélectionne le type de matière avec l'id décroissant*/
                        SELECT * FROM t_type_matiere ORDER BY id_type_matiere DESC

                /*Ajouter*/
                    /*insert le type de données*/
                    INSERT INTO t_type_matiere (id_type_matiere, type_matiere) 
                         VALUES (NULL, 'Branche')   

                /*Update*/
                    /*Update un type de matière*/
                      UPDATE t_type_matiere
                        SET type_matiere = 'Module'
                        WHERE id_type_matiere = 1
                /*Delete*/
                    /*Supprime un type de matiere*/
                       DELETE FROM t_type_matiere WHERE id_type_matiere = 1

                    /*Sélectionne toute les données de la table t_type_matiere*/   
                        SELECT * FROM t_type_matiere

            /*dossier type notes*/
                /*afficher*/
                    /*sélectionne le type de notes*/
                        SELECT * FROM t_type_notes WHERE id_type_notes = 1
                    /*Sélectionne le type de notes avec l'id décroissant*/
                        SELECT * FROM t_type_notes ORDER BY id_type_notes DESC

                /*Ajouter*/
                    /*insert le type de données*/
                    INSERT INTO t_type_matiere (id_type_notes, type_notes) 
                         VALUES (NULL, 'Moyenne')   

                /*Update*/
                    /*Update un type de notes*/
                      UPDATE t_type_notes
                        SET type_notes = 'Moyen'
                        WHERE id_type_notes = 1
                /*Delete*/
                    /*Supprime un type de notes*/
                       DELETE FROM t_type_notes WHERE id_type_notes = 1

                    /*Sélectionne toute les données de la table t_type_notes*/   
                        SELECT * FROM t_type_notes