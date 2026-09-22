import { useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { useCorpus } from '../hooks/useCorpus'

const CENTROIDS = {
  FR: [46.6, 2.2], BR: [-14.2, -51.9], UK: [55.4, -3.4], DE: [51.2, 10.4],
  IT: [41.9, 12.5], US: [37.1, -95.7], AT: [47.5, 14.6], PT: [39.4, -8.2],
  CH: [46.8, 8.2], GR: [39.1, 21.8], JP: [36.2, 138.3], ES: [40.5, -3.7],
  NL: [52.1, 5.3], BE: [50.5, 4.5], RU: [61.5, 105.3], AR: [-38.4, -63.6],
}

function markerIcon(n) {
  return L.divIcon({
    html: `<div style="background:#6B1E3A;color:#F5ECD6;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,.25);border:2px solid #C9A961">${n}</div>`,
    className: '',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  })
}

export default function Mapa() {
  const { items, loading } = useCorpus()

  const byCountry = useMemo(() => {
    const map = {}
    items.forEach(i => {
      if (!i.pais) return
      if (!map[i.pais]) map[i.pais] = { items: [], nome: i.pais_nome }
      map[i.pais].items.push(i)
    })
    return map
  }, [items])

  if (loading) return <div className="flex items-center justify-center h-[60vh]"><p className="text-[#8B7355]">Carregando mapa...</p></div>

  return (
    <div className="h-[calc(100vh-73px)] relative">
      <MapContainer center={[30, 10]} zoom={2} className="h-full w-full" scrollWheelZoom>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OSM'
          className="grayscale contrast-125"
        />
        {Object.entries(byCountry).map(([code, { items: countryItems, nome }]) => {
          const pos = CENTROIDS[code]
          if (!pos) return null
          return (
            <Marker key={code} position={pos} icon={markerIcon(countryItems.length)}>
              <Popup>
                <div className="font-sans min-w-[180px]">
                  <strong className="text-[#6B1E3A] text-sm">{nome}</strong>
                  <span className="text-[#8B7355] text-xs ml-1">({countryItems.length})</span>
                  <ul className="mt-2 text-xs space-y-1 max-h-[200px] overflow-y-auto">
                    {countryItems.slice(0, 10).map(i => (
                      <li key={i.id} className="text-[#3D2817]">{i.titulo} <span className="text-[#8B7355]">({i.data_estimada})</span></li>
                    ))}
                    {countryItems.length > 10 && <li className="text-[#8B7355] italic">+{countryItems.length - 10} mais...</li>}
                  </ul>
                </div>
              </Popup>
            </Marker>
          )
        })}
      </MapContainer>
      <div className="absolute bottom-4 left-4 z-[1000] vintage-card p-4 rounded-lg shadow-lg text-xs">
        <p className="font-serif text-lg text-[#6B1E3A] mb-1">Distribuição geográfica</p>
        <p className="text-[#8B7355]">{Object.keys(byCountry).length} países · {items.length} itens</p>
      </div>
    </div>
  )
}
