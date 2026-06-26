import rhinoscriptsyntax as  rs  # type: ignore

line = rs.GetLine()
if line: rs.AddLine( line[0],  line[1] )