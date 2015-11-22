-- wierszy, kolumn, dl, sz, x1, y1
DROP TABLE IF EXISTS ridx.grid;
CREATE TABLE ridx.grid AS 
	SELECT row_number() over(), row, 
		chr(col+64) AS col,  
		chr(col+64) || "row"::text AS idx_f, 
		geom FROM ST_CreateFishnet(20,20,1150,850,510530,249300);
--- zupełnie partyzanckie przypisanie układu
ALTER TABLE ridx.grid
  ALTER COLUMN geom TYPE geometry(POLYGON, 2180) USING ST_SetSRID(geom,2180);
