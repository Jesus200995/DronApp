# Script para actualizar iconos PWA con el icono de dron
Add-Type -AssemblyName System.Drawing

function Convert-and-Resize-Image {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [int]$Width,
        [int]$Height
    )
    
    try {
        $image = [System.Drawing.Image]::FromFile($InputPath)
        $resized = New-Object System.Drawing.Bitmap($Width, $Height)
        $graphics = [System.Drawing.Graphics]::FromImage($resized)
        
        # Configurar calidad alta
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        
        # Fondo transparente
        $graphics.Clear([System.Drawing.Color]::Transparent)
        
        # Dibujar imagen centrada
        $graphics.DrawImage($image, 0, 0, $Width, $Height)
        
        # Guardar como PNG
        $resized.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        
        $graphics.Dispose()
        $resized.Dispose()
        $image.Dispose()
        
        Write-Host "Creado: $OutputPath ($Width x $Height)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error creando $OutputPath : $_" -ForegroundColor Red
        return $false
    }
}

$InputIcon = "src\assets\imagen\icodron.jpg"
$FullInputPath = (Resolve-Path $InputIcon).Path

Write-Host "Actualizando iconos PWA con imagen de dron..." -ForegroundColor Cyan
Write-Host "Fuente: $FullInputPath" -ForegroundColor Yellow

# Verificar que existe la imagen fuente
if (-not (Test-Path $InputIcon)) {
    Write-Host "No se encuentra la imagen fuente: $InputIcon" -ForegroundColor Red
    exit 1
}

# Crear icono 192x192 para PWA
$OutputPath192 = (Join-Path $PWD "public\pwa-192x192.png")
Convert-and-Resize-Image -InputPath $FullInputPath -OutputPath $OutputPath192 -Width 192 -Height 192

# Crear icono 512x512 para PWA  
$OutputPath512 = (Join-Path $PWD "public\pwa-512x512.png")
Convert-and-Resize-Image -InputPath $FullInputPath -OutputPath $OutputPath512 -Width 512 -Height 512

Write-Host "Iconos PWA actualizados correctamente con imagen de dron" -ForegroundColor Green
Write-Host "Recuerda actualizar el cache del navegador (Ctrl+F5)" -ForegroundColor Yellow