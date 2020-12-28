Enrollment

curl -F "audio=@test_audios/john.wav" "0.0.0.0:7489/enroll?id=1556&name=john"

we can enroll multiple audio segments for same speaker by keeping `name` same and just changing the `id`

Verification

curl -F "audio=@test_audios/john.wav" "0.0.0.0:7489/enroll"
