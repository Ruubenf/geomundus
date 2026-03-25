<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>QR Panel</title>

        <style>
        body {
            display: grid;
            place-items: center;
            height: 75vh;
            margin: 0;
        }

        .success{
            background-color: green;
        }

        .btn{
            width: 35%;
            height: 10vh;
            font-size: 4rem;
        }

        .btn-outline-secondary{
            width: 35%;
            height: 10vh;
            font-size: 2rem;
        }
    </style>

</head>
<body>

    <h1>Select an event</h1>
    <h2>This is the reverse cammera menu</h2>

    <img src="logo.png" alt="logo picture" width="50%">
    <button class="btn btn-outline-primary" onclick="location.href='scan_reverse.php?action=welcome'">Welcome</button>
    <button class="btn btn-outline-primary" onclick="location.href='scan_reverse.php?action=dinner'">Dinner</button>
<br>
    <button class="btn btn-outline-secondary" onclick="location.href='scan_reverse.php?action=digital_twins_(nicolas)'">Digital Twins (Nicolas Luna)</button>
    <button class="btn btn-outline-secondary" onclick="location.href='scan_reverse.php?action=participatory_mapping_(candela)'">Participatory Mapping (Candela Sol)</button>
    <button class="btn btn-outline-secondary" onclick="location.href='scan_reverse.php?action=disaster_management_(andres)'">Disaster Management (Andrés Ramírez)</button>
</body>
</html>
