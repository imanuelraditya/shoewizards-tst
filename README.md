# shoewizards-tst
Microservice yang akan diimplementasikan dalam API ini merupakan core dari bisnis yang dibuat, yaitu konsultasi produk pemeliharaan yang cocok untuk sepatu pelangan. Nantinya ketika pelanggan akan memanfaatkan jasa pemeliharaan sepatu, data pelanggan, yang berisi berbagai informasi relevan mengenai pelanggan, akan disimpan ke dalam tabel customer, sementara data sepatunya akan disimpan ke dalam tabel shoes. Nantinya, dari ID pelanggan dan ID sepatu yang telah didaftarkan oleh pelanggan, akan di-generate berbagai produk pemeliharaan dari tabel products yang cocok dan sesuai dengan sepatu pengguna. Data hasil konsultasi ini nantinya disimpan ke dalam tabel consultations yang mencatat ID pelanggan, ID sepatu, ID produk, dan tanggal konsultasi. Jadi, total layanan ini memiliki empat buah tabel.

Namun, agar layanan ini bisa memberikan fungsionalitas yang lebih menyeluruh, maka akan dilakukan integrasi dengan layanan SmartCart. Dengan layanan SmartCart, pengguna akan dimungkinkan untuk langsung memesan dan membeli produk hasil rekomendasi

# URL Link
API Documentation	: https://shoewizardsdb.azurewebsites.net/
Github Backend	: https://github.com/imanuelraditya/shoewizards-tst
Github Frontend	: https://github.com/imanuelraditya/shoewizards-tst-frontend
Website	: https://shoewizards-tst-frontend-git-main-imanuelradityas-projects.vercel.app/

# Tech Stack Backend
Programming language: Python
Cloud Database: Azure MySQL
Authentication: OAuth, JWT
Container: Docker
Hosting: Microsoft Azure

# Tech Stack Backend
Programming language: TypeScript
React
Framework: FlowBite
Data Fetch: Axios
