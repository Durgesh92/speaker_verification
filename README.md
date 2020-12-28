Enrollment

curl -F "audio=@test_audios/john.wav" "0.0.0.0:7489/enroll?id=1556&name=john"


Verification

curl -F "audio=@test_audios/john.wav" "0.0.0.0:7489/enroll"
