## Giriş

Google tarafından geliştirilen "mediapipe" paketi, kullanıcının elini algılamak ve 21 dönüm noktasını belirlemek için kullanılır. Bu dönüm noktalarının koordinatları, videoda doğru bir konum belirlemek için kullanılır. Ayrıca, OpenCV modülü kullanılarak yapılan harekete dayalı çizim, silme gibi işlevler de mevcuttur. Kullanıcılar, fırça rengi, silgi rengi ve boyutları gibi çeşitli özellikleri özelleştirebilir.

## Uygulama Aşamaları

### 1. Videonun İşlenmesi

Web kamerası aracılığıyla alınan video, Python'da bulunan OpenCV modülü ile işlenir. Varsayılan olarak yatay ters çevirme olmadığı için, videonun ters çevrilmesi gerekir. Aksi takdirde, yazılan metin de ters görünecektir.

### 2. Hareket Tanıma Nesnesinin Oluşturulması

Mediapipe modülünde bulunan sınıf nesnesi, kullanıcının elini algılamak ve 21 dönüm noktasının koordinatlarını liste olarak döndürmek için kullanılır. Elde edilen koordinatlar, çeşitli işlevlere atanabilir.

### 3. Video Akışında Çizim Yapma

Elde edilen koordinatlar kullanılarak, OpenCV modülü ile doğru bir şekilde çizim yapılabilir. Fırça kalınlığı, rengi, silgi boyutu gibi özellikler ayarlanabilir.

## Kullanım

1. **İşaret Parmağı:** Videoya çizim yapmak için kullanılır.

2. **İndeks + Orta Parmak:** Videoda gezinmek ve gezinme çubuğunu kullanmak için kullanılır.

3. **İndeks + Orta + Yüzük + Küçük Parmak:** Yazılı metni silmek için kullanılır.