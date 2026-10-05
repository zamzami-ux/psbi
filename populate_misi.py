import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from dashboard.models import Mission, Question, Choice

def run():
    Mission.objects.all().delete()

    # ===== MISI 1: Pengenalan Gambar Vektor vs Raster =====
    m1 = Mission.objects.create(
        title="Pengenalan Gambar Vektor vs Raster",
        description="Pahami perbedaan mendasar antara grafis vektor dan raster serta kapan menggunakan masing-masing.",
        xp_reward=100,
        content="""
        <h2>Apa Itu Gambar Vektor?</h2>
        <p>Gambar <strong>vektor</strong> adalah jenis grafis digital yang dibuat menggunakan rumus matematika berupa titik, garis, kurva, dan bentuk geometris. Karena berbasis matematika, gambar vektor dapat diperbesar atau diperkecil tanpa kehilangan kualitas (tidak pecah/blur).</p>

        <h3>Apa Itu Gambar Raster?</h3>
        <p>Gambar <strong>raster</strong> (atau bitmap) tersusun dari kumpulan piksel — titik-titik kecil berwarna yang membentuk sebuah gambar. Setiap piksel memiliki informasi warna tersendiri. Contoh format raster: JPG, PNG, BMP, GIF.</p>

        <h3>Perbedaan Utama</h3>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Aspek</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Vektor</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Raster</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Basis</td>
                <td style="padding: 12px;">Rumus matematika</td>
                <td style="padding: 12px;">Piksel</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Skalabilitas</td>
                <td style="padding: 12px;">Tidak pecah saat diperbesar</td>
                <td style="padding: 12px;">Pecah/blur saat diperbesar</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Ukuran File</td>
                <td style="padding: 12px;">Relatif kecil</td>
                <td style="padding: 12px;">Bisa sangat besar</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Contoh Format</td>
                <td style="padding: 12px;">SVG, AI, EPS, CDR</td>
                <td style="padding: 12px;">JPG, PNG, BMP, GIF</td>
            </tr>
        </table>

        <h3>Kapan Menggunakan Vektor?</h3>
        <ul>
            <li><strong>Logo dan branding</strong> — perlu tampil konsisten di berbagai ukuran</li>
            <li><strong>Ikon dan ilustrasi</strong> — butuh ketajaman di resolusi apapun</li>
            <li><strong>Tipografi kustom</strong> — huruf yang bisa diskalakan</li>
            <li><strong>Desain cetak</strong> — billboard, spanduk, kartu nama</li>
        </ul>

        <h3>Kapan Menggunakan Raster?</h3>
        <ul>
            <li><strong>Fotografi</strong> — detail warna yang kompleks</li>
            <li><strong>Editing foto</strong> — manipulasi piksel per piksel</li>
            <li><strong>Tekstur detail</strong> — gradasi warna yang halus</li>
        </ul>
        """,
        order=1
    )

    q1 = Question.objects.create(mission=m1, text="Apa yang menjadi basis dari gambar vektor?", order=1)
    Choice.objects.create(question=q1, text="Piksel", is_correct=False)
    Choice.objects.create(question=q1, text="Rumus matematika (titik, garis, kurva)", is_correct=True)
    Choice.objects.create(question=q1, text="Kumpulan foto", is_correct=False)
    Choice.objects.create(question=q1, text="Layer bitmap", is_correct=False)

    q2 = Question.objects.create(mission=m1, text="Apa yang terjadi pada gambar vektor saat diperbesar?", order=2)
    Choice.objects.create(question=q2, text="Gambar menjadi pecah/blur", is_correct=False)
    Choice.objects.create(question=q2, text="Ukuran file membesar drastis", is_correct=False)
    Choice.objects.create(question=q2, text="Gambar tetap tajam tanpa kehilangan kualitas", is_correct=True)
    Choice.objects.create(question=q2, text="Warna gambar berubah", is_correct=False)

    # ===== MISI 2: Tools Desain Vektor =====
    m2 = Mission.objects.create(
        title="Tools Desain Vektor",
        description="Kenali software populer untuk membuat desain vektor: Inkscape, Adobe Illustrator, dan CorelDRAW.",
        xp_reward=100,
        content="""
        <h2>Software Desain Vektor Populer</h2>
        <p>Ada banyak software untuk membuat gambar vektor. Berikut tiga yang paling populer:</p>

        <h3>1. Adobe Illustrator</h3>
        <p>Adobe Illustrator adalah software desain vektor <strong>standar industri</strong> yang digunakan oleh desainer profesional di seluruh dunia. Fitur unggulannya antara lain:</p>
        <ul>
            <li>Pen Tool yang sangat presisi</li>
            <li>Integrasi sempurna dengan Adobe Creative Cloud</li>
            <li>Library simbol dan brush yang sangat lengkap</li>
            <li>Mendukung format AI, EPS, SVG, PDF</li>
        </ul>

        <h3>2. Inkscape</h3>
        <p>Inkscape adalah alternatif <strong>gratis dan open-source</strong> untuk desain vektor. Cocok untuk pemula dan profesional:</p>
        <ul>
            <li>Mendukung format SVG secara native</li>
            <li>Tersedia di Windows, macOS, dan Linux</li>
            <li>Fitur path editing yang powerful</li>
            <li>Komunitas dan plugin yang aktif</li>
        </ul>

        <h3>3. CorelDRAW</h3>
        <p>CorelDRAW adalah software desain vektor yang sangat populer di Indonesia, terutama untuk <strong>desain cetak dan percetakan</strong>:</p>
        <ul>
            <li>Antarmuka yang intuitif dan mudah dipelajari</li>
            <li>PowerTRACE untuk konversi bitmap ke vektor</li>
            <li>Fitur layout multi-halaman</li>
            <li>Format native CDR</li>
        </ul>

        <h3>Perbandingan Singkat</h3>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Software</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Harga</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Keunggulan</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Adobe Illustrator</td>
                <td style="padding: 12px;">Berbayar (langganan)</td>
                <td style="padding: 12px;">Standar industri, fitur lengkap</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Inkscape</td>
                <td style="padding: 12px;">Gratis</td>
                <td style="padding: 12px;">Open-source, SVG native</td>
            </tr>
            <tr>
                <td style="padding: 12px;">CorelDRAW</td>
                <td style="padding: 12px;">Berbayar</td>
                <td style="padding: 12px;">Populer di percetakan Indonesia</td>
            </tr>
        </table>
        """,
        order=2
    )

    q3 = Question.objects.create(mission=m2, text="Manakah software desain vektor yang gratis dan open-source?", order=1)
    Choice.objects.create(question=q3, text="Adobe Illustrator", is_correct=False)
    Choice.objects.create(question=q3, text="CorelDRAW", is_correct=False)
    Choice.objects.create(question=q3, text="Inkscape", is_correct=True)
    Choice.objects.create(question=q3, text="Photoshop", is_correct=False)

    q4 = Question.objects.create(mission=m2, text="Software vektor apa yang paling populer di percetakan Indonesia?", order=2)
    Choice.objects.create(question=q4, text="Inkscape", is_correct=False)
    Choice.objects.create(question=q4, text="CorelDRAW", is_correct=True)
    Choice.objects.create(question=q4, text="GIMP", is_correct=False)
    Choice.objects.create(question=q4, text="Canva", is_correct=False)

    # ===== MISI 3: Bezier Curves, Paths & Shapes =====
    m3 = Mission.objects.create(
        title="Bezier Curves, Paths & Shapes",
        description="Pelajari dasar-dasar kurva Bezier, paths, dan shapes yang menjadi fondasi gambar vektor.",
        xp_reward=100,
        content="""
        <h2>Memahami Bezier Curves</h2>
        <p><strong>Bezier curve</strong> (kurva Bezier) adalah kurva matematis yang digunakan sebagai dasar pembuatan gambar vektor. Kurva ini ditemukan oleh Pierre Bézier pada tahun 1960-an untuk desain bodi mobil Renault.</p>

        <h3>Komponen Bezier Curve</h3>
        <ul>
            <li><strong>Anchor Point (Titik Jangkar):</strong> Titik awal dan akhir dari sebuah segmen kurva</li>
            <li><strong>Handle/Control Point:</strong> Titik kontrol yang menentukan bentuk lengkungan kurva</li>
            <li><strong>Path Segment:</strong> Garis atau kurva yang menghubungkan dua anchor point</li>
        </ul>

        <h3>Jenis-jenis Bezier Curve</h3>
        <ul>
            <li><strong>Linear (Garis Lurus):</strong> Dua anchor point tanpa handle — menghasilkan garis lurus</li>
            <li><strong>Quadratic Bezier:</strong> Menggunakan satu control point — kurva sederhana</li>
            <li><strong>Cubic Bezier:</strong> Menggunakan dua control point — kurva yang lebih kompleks dan fleksibel (paling sering digunakan)</li>
        </ul>

        <h3>Path (Jalur)</h3>
        <p>Path adalah rangkaian dari beberapa Bezier curve yang saling terhubung. Ada dua jenis path:</p>
        <ul>
            <li><strong>Open Path:</strong> Jalur terbuka — titik awal dan akhir berbeda (contoh: garis, kurva)</li>
            <li><strong>Closed Path:</strong> Jalur tertutup — titik awal dan akhir bertemu (contoh: lingkaran, kotak)</li>
        </ul>

        <h3>Shapes (Bentuk Dasar)</h3>
        <p>Shapes adalah bentuk-bentuk geometris dasar yang sudah disediakan di software vektor:</p>
        <ul>
            <li><strong>Rectangle/Rounded Rectangle</strong> — Persegi dan persegi panjang</li>
            <li><strong>Ellipse/Circle</strong> — Elips dan lingkaran</li>
            <li><strong>Polygon</strong> — Segitiga, segi lima, bintang, dll</li>
            <li><strong>Line/Arrow</strong> — Garis dan panah</li>
        </ul>
        <p>Semua shapes pada dasarnya adalah closed paths yang bisa diedit menggunakan anchor points.</p>

        <h3>Tips Menggunakan Pen Tool</h3>
        <ul>
            <li>Klik untuk membuat anchor point dengan garis lurus</li>
            <li>Klik dan drag untuk membuat anchor point dengan kurva</li>
            <li>Gunakan seminimal mungkin anchor points untuk hasil yang smooth</li>
            <li>Tahan Alt/Option untuk mengatur handle secara independen</li>
        </ul>
        """,
        order=3
    )

    q5 = Question.objects.create(mission=m3, text="Apa fungsi dari Handle/Control Point pada Bezier curve?", order=1)
    Choice.objects.create(question=q5, text="Menentukan warna garis", is_correct=False)
    Choice.objects.create(question=q5, text="Menentukan bentuk lengkungan kurva", is_correct=True)
    Choice.objects.create(question=q5, text="Menentukan ketebalan garis", is_correct=False)
    Choice.objects.create(question=q5, text="Menentukan ukuran file", is_correct=False)

    q6 = Question.objects.create(mission=m3, text="Apa perbedaan antara Open Path dan Closed Path?", order=2)
    Choice.objects.create(question=q6, text="Open path berwarna, closed path tidak", is_correct=False)
    Choice.objects.create(question=q6, text="Open path titik awal dan akhirnya berbeda, closed path titik awal dan akhirnya bertemu", is_correct=True)
    Choice.objects.create(question=q6, text="Open path hanya bisa garis lurus", is_correct=False)
    Choice.objects.create(question=q6, text="Closed path tidak bisa diedit", is_correct=False)

    # ===== MISI 4: Typography Vektor =====
    m4 = Mission.objects.create(
        title="Typography Vektor",
        description="Pelajari bagaimana tipografi bekerja dalam dunia vektor dan teknik manipulasi teks.",
        xp_reward=100,
        content="""
        <h2>Typography dalam Desain Vektor</h2>
        <p>Tipografi vektor adalah seni dan teknik menggunakan huruf (teks) dalam format vektor. Font yang kita gunakan sehari-hari sebenarnya adalah kumpulan <strong>kurva Bezier</strong> yang membentuk setiap karakter huruf.</p>

        <h3>Mengapa Tipografi Vektor Penting?</h3>
        <ul>
            <li><strong>Skalabilitas:</strong> Teks tetap tajam di ukuran apapun</li>
            <li><strong>Editabilitas:</strong> Mudah diubah warna, ukuran, dan bentuknya</li>
            <li><strong>Konsistensi:</strong> Tampilan seragam di berbagai media</li>
            <li><strong>Print-ready:</strong> Siap cetak di resolusi tinggi</li>
        </ul>

        <h3>Konsep Dasar Typography</h3>
        <ul>
            <li><strong>Typeface vs Font:</strong> Typeface adalah keluarga desain huruf (misal: Arial), sedangkan Font adalah variasi spesifik (misal: Arial Bold 12pt)</li>
            <li><strong>Serif vs Sans-serif:</strong> Serif memiliki kaki/ekor di ujung huruf (Times New Roman), Sans-serif tidak (Helvetica)</li>
            <li><strong>Kerning:</strong> Jarak antar karakter individual</li>
            <li><strong>Leading:</strong> Jarak antar baris teks</li>
            <li><strong>Tracking:</strong> Jarak keseluruhan antar huruf dalam satu kata/kalimat</li>
        </ul>

        <h3>Teknik Typography Vektor</h3>
        <ul>
            <li><strong>Convert to Outlines/Curves:</strong> Mengubah teks menjadi path vektor — teks tidak bisa diedit lagi tapi bisa dimanipulasi bentuknya</li>
            <li><strong>Text on Path:</strong> Menempatkan teks mengikuti jalur kurva</li>
            <li><strong>Text Wrap:</strong> Membuat teks mengalir mengikuti bentuk objek</li>
            <li><strong>Custom Lettering:</strong> Membuat huruf kustom menggunakan Pen Tool</li>
        </ul>

        <h3>Tips Praktis</h3>
        <ul>
            <li>Selalu convert text to outlines sebelum mengirim file ke percetakan</li>
            <li>Gunakan maksimal 2-3 jenis font dalam satu desain</li>
            <li>Perhatikan hierarki visual: judul, subjudul, body text</li>
            <li>Pastikan kontras warna teks dengan background cukup tinggi</li>
        </ul>
        """,
        order=4
    )

    q7 = Question.objects.create(mission=m4, text="Apa yang dimaksud dengan 'Convert to Outlines/Curves' pada teks?", order=1)
    Choice.objects.create(question=q7, text="Mengubah warna teks", is_correct=False)
    Choice.objects.create(question=q7, text="Mengubah teks menjadi path vektor yang bisa dimanipulasi bentuknya", is_correct=True)
    Choice.objects.create(question=q7, text="Menghapus teks dari desain", is_correct=False)
    Choice.objects.create(question=q7, text="Membuat teks menjadi 3D", is_correct=False)

    q8 = Question.objects.create(mission=m4, text="Apa perbedaan antara Kerning dan Tracking?", order=2)
    Choice.objects.create(question=q8, text="Kerning untuk jarak antar baris, Tracking untuk jarak antar huruf", is_correct=False)
    Choice.objects.create(question=q8, text="Kerning untuk jarak antar karakter individual, Tracking untuk jarak keseluruhan antar huruf", is_correct=True)
    Choice.objects.create(question=q8, text="Keduanya sama saja", is_correct=False)
    Choice.objects.create(question=q8, text="Kerning untuk ukuran huruf, Tracking untuk warna huruf", is_correct=False)

    # ===== MISI 5: Ekspor dan Format File Vektor =====
    m5 = Mission.objects.create(
        title="Ekspor & Format File Vektor",
        description="Kenali berbagai format file vektor (SVG, AI, EPS) dan cara mengekspornya dengan benar.",
        xp_reward=100,
        content="""
        <h2>Format File Vektor</h2>
        <p>Mengetahui format file yang tepat sangat penting agar karya vektor dapat digunakan di berbagai kebutuhan. Berikut format-format utama:</p>

        <h3>1. SVG (Scalable Vector Graphics)</h3>
        <ul>
            <li>Format vektor berbasis XML</li>
            <li>Standar terbuka oleh W3C</li>
            <li><strong>Ideal untuk web</strong> — didukung semua browser modern</li>
            <li>Bisa diedit dengan text editor karena berbasis kode</li>
            <li>Mendukung animasi dan interaktivitas</li>
        </ul>

        <h3>2. AI (Adobe Illustrator)</h3>
        <ul>
            <li>Format native Adobe Illustrator</li>
            <li>Menyimpan semua fitur: layer, efek, mask, dll</li>
            <li>Standar industri desain profesional</li>
            <li>Hanya bisa dibuka sempurna di Adobe Illustrator</li>
        </ul>

        <h3>3. EPS (Encapsulated PostScript)</h3>
        <ul>
            <li>Format vektor legacy yang masih banyak digunakan</li>
            <li><strong>Standar untuk percetakan</strong></li>
            <li>Kompatibel dengan banyak software desain</li>
            <li>Bisa berisi vektor dan raster sekaligus</li>
        </ul>

        <h3>4. PDF (Portable Document Format)</h3>
        <ul>
            <li>Bisa menyimpan data vektor dengan sempurna</li>
            <li>Universal — bisa dibuka di hampir semua perangkat</li>
            <li>Cocok untuk print dan distribusi digital</li>
        </ul>

        <h3>5. CDR (CorelDRAW)</h3>
        <ul>
            <li>Format native CorelDRAW</li>
            <li>Populer di Indonesia untuk percetakan</li>
            <li>Hanya bisa dibuka sempurna di CorelDRAW</li>
        </ul>

        <h3>Panduan Ekspor</h3>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Kebutuhan</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Format</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Website / Aplikasi</td>
                <td style="padding: 12px;">SVG</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Cetak profesional</td>
                <td style="padding: 12px;">EPS atau PDF</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Kolaborasi tim desain</td>
                <td style="padding: 12px;">AI atau CDR</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Sharing universal</td>
                <td style="padding: 12px;">PDF</td>
            </tr>
        </table>

        <h3>Tips Ekspor</h3>
        <ul>
            <li>Selalu simpan file sumber (AI/CDR) sebelum mengekspor ke format lain</li>
            <li>Convert text to outlines sebelum ekspor untuk menghindari masalah font</li>
            <li>Untuk web, optimasi SVG dengan tools seperti SVGO</li>
            <li>Untuk cetak, pastikan color mode CMYK dan resolusi minimal 300 DPI</li>
        </ul>
        """,
        order=5
    )

    q9 = Question.objects.create(mission=m5, text="Format vektor apa yang paling ideal untuk digunakan di website?", order=1)
    Choice.objects.create(question=q9, text="AI", is_correct=False)
    Choice.objects.create(question=q9, text="EPS", is_correct=False)
    Choice.objects.create(question=q9, text="SVG", is_correct=True)
    Choice.objects.create(question=q9, text="CDR", is_correct=False)

    q10 = Question.objects.create(mission=m5, text="Apa yang harus dilakukan sebelum mengekspor file vektor ke percetakan?", order=2)
    Choice.objects.create(question=q10, text="Mengubah ke format GIF", is_correct=False)
    Choice.objects.create(question=q10, text="Convert text to outlines dan pastikan color mode CMYK", is_correct=True)
    Choice.objects.create(question=q10, text="Menghapus semua layer", is_correct=False)
    Choice.objects.create(question=q10, text="Mengubah resolusi ke 72 DPI", is_correct=False)

    print("5 misi gambar vektor berhasil ditambahkan!")
    print(f"   Total misi: {Mission.objects.count()}")
    print(f"   Total soal: {Question.objects.count()}")
    print(f"   Total pilihan: {Choice.objects.count()}")

if __name__ == '__main__':
    run()
