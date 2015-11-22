\timing on
DROP TABLE IF EXISTS ridx.drogi_jednostka;
-- wyszukaj id jednostki nadrzednej (powiatu)
CREATE TABLE ridx.drogi_jednostka AS (WITH powiat AS (SELECT geometry FROM import.osm_admin WHERE "teryt:terc"='2468'),
drogi AS (SELECT osm_id, geometry, name FROM import.osm_roads WHERE "name"!='' AND "class"='highway' AND "type" NOT IN ('motorway','motorway_link','proposed'))
SELECT *, ''::text AS gmina, ''::text AS solectwo FROM drogi WHERE ST_Intersects((SELECT geometry FROM powiat), drogi.geometry) AND NOT ST_Touches((SELECT geometry FROM powiat), drogi.geometry));

UPDATE ridx.drogi_jednostka t SET gmina = (select string_agg(name, ',') FROM import.osm_admin p where admin_level = '7' and st_intersects(t.geometry, p.geometry) and not st_touches(t.geometry, p.geometry));
--UPDATE ridx.drogi_jednostka t SET solectwo = (select string_agg(name, ',') FROM import.osm_admin p where admin_level = '9' and st_intersects(t.geometry, p.geometry) and not st_touches(t.geometry, p.geometry));

DROP TABLE IF EXISTS ridx.drogi_wsie;
CREATE TABLE ridx.drogi_wsie AS
    SELECT row_number() OVER (), name, solectwo, gmina, ST_LineMerge(ST_Collect(geometry)) AS geometry FROM ridx.drogi_jednostka t GROUP BY name, solectwo, gmina;
DROP TABLE IF EXISTS ridx.drogi_indeks;
CREATE TABLE ridx.drogi_indeks AS SELECT geometry, name, solectwo, gmina, (select string_agg(idx_f, ',') from (select idx_f from ridx.grid p WHERE st_intersects(t.geometry, ST_Transform(p.geom,3857))) AS foo) AS idx_f FROM ridx.drogi_wsie t ORDER BY gmina, solectwo, name;
-- wskaz sciezke dostepu dla pliku eksportu
\COPY ridx.drogi_indeks(name, solectwo, gmina, idx_f) TO '/home/mechanik/dev/Projekty/Jaworzno/csv/indeks.csv' WITH ENCODING 'UTF-8' DELIMITER ';'
