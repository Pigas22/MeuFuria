import instaloader
import os 
import shutil


def baixar_postagens_instagram(username: str, qtd_posts: int = 5):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)

    for num_post, post in enumerate(profile.get_posts()):
        frase_chave = post.caption.lower().split('\n')[0].strip().split(' ')

        for plvr in frase_chave:
            if len(plvr) >= 3:
                plvr_chave_post = plvr
                break

        pasta_origem = f'{profile.username}-{plvr_chave_post}-{post.date_utc.date()}'
        pasta_destino = os.path.join('src', 'data', f'{profile.username}', f'Post-{plvr_chave_post}-{post.date_utc.date()}')

        if os.path.isdir(pasta_destino):
            print('Postagem já baixada')
        
        else: 
            os.makedirs(pasta_destino, exist_ok=True)
            L.download_post(post, target=pasta_origem)

            arquivos = os.listdir(pasta_origem)


            dict_arqv = {
                'extensoes': ['.txt', '.jpg', '.mp4', '.json.xz'],
                'tipo': ['Descrição', 'Imagem', 'Video', 'ArqJson'],
                'qtd': [0, 0, 0, 0]
            }

            extensoes = ['.txt', '.jpg', '.mp4', '.json.xz']
            tipos = ['Descrição', 'Imagem', 'Video', 'ArqJson']
            qtd = [0, 0, 0, 0]
            for arq in arquivos:
                arq_renomeado = arq

                for i, ex in enumerate(extensoes):
                    if (arq.endswith(ex)):
                        if qtd[i] > 0:
                            arq_renomeado = tipos[i] + f'{qtd[i]}' + ex
                        
                        else:
                            arq_renomeado = tipos[i] + ex

                        qtd[i] += 1

                print(qtd)

                caminho_arq_origem = os.path.join(pasta_origem, arq)
                caminho_arq_dest = os.path.join(pasta_destino, arq_renomeado)

                shutil.move(caminho_arq_origem, caminho_arq_dest)
            
            os.removedirs(pasta_origem)

            print('Postagem baixada agora!')

        if num_post == (qtd_posts-1):
            break


if __name__ == '__main__':
    baixar_postagens_instagram('furiagg', 6)