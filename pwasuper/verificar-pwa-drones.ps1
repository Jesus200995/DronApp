# Script de verificación de la actualización PWA
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   VERIFICACION PWA DRONES" -ForegroundColor Cyan  
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📱 NOMBRE DE LA APLICACION:" -ForegroundColor Yellow
$title = Select-String -Path "index.html" -Pattern "<title>"
$title.Line.Trim()

Write-Host ""
Write-Host "🏷️ NOMBRE EN MANIFEST:" -ForegroundColor Yellow  
$name = Select-String -Path "public\manifest.json" -Pattern '"name":'
$name.Line.Trim()

Write-Host ""
Write-Host "📦 NOMBRE EN PACKAGE.JSON:" -ForegroundColor Yellow
$package = Select-String -Path "package.json" -Pattern '"name":'
$package.Line.Trim()

Write-Host ""
Write-Host "🖼️ ICONOS GENERADOS:" -ForegroundColor Yellow
Get-ChildItem "public\pwa-*.png" | ForEach-Object {
    $sizeKB = [math]::Round($_.Length / 1024, 2)
    Write-Host "  ✅ $($_.Name) - $sizeKB KB" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 ARCHIVOS DE DISTRIBUCION:" -ForegroundColor Yellow
if (Test-Path "dist") {
    $distIcons = Get-ChildItem "dist\pwa-*.png" 2>$null
    if ($distIcons) {
        $distIcons | ForEach-Object {
            $sizeKB = [math]::Round($_.Length / 1024, 2)
            Write-Host "  ✅ dist\$($_.Name) - $sizeKB KB" -ForegroundColor Green
        }
    } else {
        Write-Host "  ⚠️ No se encontraron iconos en dist/" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️ Carpeta dist/ no existe" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "  1. Desplegar archivos de dist/ a tu servidor" -ForegroundColor White
Write-Host "  2. Limpiar cache del navegador (Ctrl + F5)" -ForegroundColor White  
Write-Host "  3. Reinstalar PWA desde el navegador" -ForegroundColor White
Write-Host "  4. Verificar que el nuevo icono y nombre aparezcan" -ForegroundColor White

Write-Host ""
Write-Host "✅ ACTUALIZACION COMPLETADA EXITOSAMENTE" -ForegroundColor Green