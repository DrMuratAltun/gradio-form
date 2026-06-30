import os
import gradio as gr
import pandas as pd

# CSV dosya yolu
CSV_PATH = "/Users/drmurataltun/Documents/gradio-form/form.csv"

# Varsayılan kolonlar
COLUMNS = ["Ad", "Soyad", "E-posta", "Yaş", "Cinsiyet", "Bölüm", "İş durumu"]

def load_records():
    """CSV dosyasındaki tüm kayıtları okur ve DataFrame olarak döndürür."""
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH, encoding="utf-8")
            # Kolonların eşleştiğinden emin olalım
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUMNS]
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {e}")
            return pd.DataFrame(columns=COLUMNS)
    else:
        # Dosya yoksa boş bir şablon oluştur
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_PATH, index=False, encoding="utf-8")
        return df

def add_record(first_name, last_name, email, age, gender, department, employment_status):
    """Yeni bir kaydı doğrular, CSV dosyasına kaydeder ve güncel tabloyu döndürür."""
    # Girdi Doğrulamaları
    if not first_name or not first_name.strip():
        return gr.update(value="⚠️ Hata: 'Ad' alanı boş bırakılamaz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status
    
    if not last_name or not last_name.strip():
        return gr.update(value="⚠️ Hata: 'Soyad' alanı boş bırakılamaz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status
        
    if not email or not email.strip() or "@" not in email:
        return gr.update(value="⚠️ Hata: Geçerli bir 'E-posta' adresi giriniz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

    if age is None or age <= 0 or age > 120:
        return gr.update(value="⚠️ Hata: Geçerli bir 'Yaş' değeri giriniz (1-120)!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

    if not gender:
        return gr.update(value="⚠️ Hata: Lütfen 'Cinsiyet' seçiniz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

    if not department:
        return gr.update(value="⚠️ Hata: Lütfen 'Bölüm' seçiniz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

    if not employment_status:
        return gr.update(value="⚠️ Hata: Lütfen 'İş Durumu' seçiniz!", visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

    # Yeni veriyi hazırlayalım
    new_data = {
        "Ad": first_name.strip(),
        "Soyad": last_name.strip(),
        "E-posta": email.strip(),
        "Yaş": int(age),
        "Cinsiyet": gender,
        "Bölüm": department,
        "İş durumu": employment_status
    }
    
    try:
        # Mevcut verileri yükle
        df = load_records()
        # Yeni satırı ekle
        new_df = pd.DataFrame([new_data])
        df = pd.concat([df, new_df], ignore_index=True)
        # CSV dosyasına kaydet
        df.to_csv(CSV_PATH, index=False, encoding="utf-8")
        
        success_message = f"🎉 Kayıt Başarıyla Eklendi: {first_name.strip()} {last_name.strip()}"
        
        # Formu temizle ve güncel verileri döndür
        return (
            gr.update(value=success_message, visible=True), 
            df, 
            "",  # Ad temizleme
            "",  # Soyad temizleme
            "",  # E-posta temizleme
            None,  # Yaş temizleme
            None,  # Cinsiyet temizleme
            None,  # Bölüm temizleme
            None   # İş durumu temizleme
        )
    except Exception as e:
        error_message = f"❌ Kaydedilirken bir hata oluştu: {str(e)}"
        return gr.update(value=error_message, visible=True), gr.update(), first_name, last_name, email, age, gender, department, employment_status

# Arayüz için seçenek havuzları
GENDER_OPTIONS = ["Erkek", "Kadın"]
DEPARTMENT_OPTIONS = [
    "Veri Bilimi", 
    "Bilişim Sistemleri", 
    "Yazılım Mühendisliği", 
    "Yapay Zeka Mühendisliği", 
    "Bilgisayar Mühendisliği", 
    "Makine Öğrenmesi"
]
EMPLOYMENT_OPTIONS = [
    "Yapay zekaya kaptırmadı (şimdilik)", 
    "İş Arıyor", 
    "Çalışıyor", 
    "Freelance", 
    "Öğrenci"
]

# Özel premium tasarım için CSS
custom_css = """
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
.header {
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #e056fd, #f0932b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.submit-btn {
    background: linear-gradient(135deg, #f0932b, #ff7979) !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(240, 147, 43, 0.4) !important;
}
"""

# Gradio Blocks ile modern UI oluşturma
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="slate", neutral_hue="slate"), css=custom_css) as demo:
    
    with gr.Column(elem_classes="container"):
        
        # Başlık Bölümü
        gr.Markdown(
            """
            # 📋 Kayıt ve Veri Yönetim Paneli
            Aşağıdaki formu kullanarak yeni bir kullanıcı kaydedebilir ve mevcut kayıt listesini anlık olarak takip edebilirsiniz.
            """,
            elem_classes="header"
        )
        
        # Bildirim ve Durum Mesaj Alanı
        status_box = gr.Markdown(visible=False)
        
        with gr.Tabs():
            # Kayıt Giriş Formu Sekmesi
            with gr.Tab("👤 Yeni Kayıt Ekle"):
                with gr.Column():
                    gr.Markdown("### 👤 Yeni Kayıt Bilgileri")
                    
                    with gr.Group():
                        first_name_input = gr.Textbox(
                            label="Ad", 
                            placeholder="Kullanıcının adı...", 
                            max_lines=1
                        )
                        last_name_input = gr.Textbox(
                            label="Soyad", 
                            placeholder="Kullanıcının soyadı...", 
                            max_lines=1
                        )
                        email_input = gr.Textbox(
                            label="E-posta", 
                            placeholder="ornak@alanadi.com...", 
                            max_lines=1
                        )
                        age_input = gr.Number(
                            label="Yaş", 
                            minimum=1, 
                            maximum=120, 
                            step=1,
                            precision=0
                        )
                        gender_input = gr.Dropdown(
                            choices=GENDER_OPTIONS, 
                            label="Cinsiyet", 
                            interactive=True
                        )
                        department_input = gr.Dropdown(
                            choices=DEPARTMENT_OPTIONS, 
                            label="Bölüm", 
                            interactive=True
                        )
                        employment_input = gr.Dropdown(
                            choices=EMPLOYMENT_OPTIONS, 
                            label="İş Durumu", 
                            interactive=True
                        )
                    
                    submit_button = gr.Button("Bilgileri Kaydet", elem_classes="submit-btn")
            
            # Güncel Tablo Listesi Sekmesi
            with gr.Tab("📊 Mevcut Kayıtlar"):
                with gr.Column():
                    gr.Markdown("### 📊 Mevcut Kayıtlar")
                    
                    # Başlangıçta verileri yükle
                    initial_df = load_records()
                    table_view = gr.Dataframe(
                        value=initial_df,
                        headers=COLUMNS,
                        datatype=["str", "str", "str", "number", "str", "str", "str"],
                        col_count=(len(COLUMNS), "fixed"),
                        interactive=False,
                        wrap=True
                    )
                    
                    # Tablo Yenileme Butonu
                    refresh_btn = gr.Button("🔄 Listeyi Yenile", size="sm")

        # Buton tıklama olayları
        submit_button.click(
            fn=add_record,
            inputs=[
                first_name_input, 
                last_name_input, 
                email_input, 
                age_input, 
                gender_input, 
                department_input, 
                employment_input
            ],
            outputs=[
                status_box,
                table_view,
                first_name_input,
                last_name_input,
                email_input,
                age_input,
                gender_input,
                department_input,
                employment_input
            ]
        )
        
        # Manuel yenileme tetikleyicisi
        refresh_btn.click(
            fn=load_records,
            inputs=[],
            outputs=[table_view]
        )

# Uygulamayı başlat
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
