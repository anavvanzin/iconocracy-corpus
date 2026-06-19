import { IconocracyCorpusSdk } from 'iconocracy-corpus-sdk';

(async () => {
  const iconocracyCorpusSdk = new IconocracyCorpusSdk({});

  const data = await iconocracyCorpusSdk.get_.getData();

  console.log(data);
})();
