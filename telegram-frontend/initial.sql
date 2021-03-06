PGDMP                  	         w            postgres    11.1 (Debian 11.1-1.pgdg90+1)    11.1     N           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            O           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            P           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            Q           1262    13065    postgres    DATABASE     x   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
    DROP DATABASE postgres;
             postgres    false            R           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                  postgres    false    2897            �            1259    24591    events    TABLE     �   CREATE TABLE public.events (
    event_id smallint NOT NULL,
    gate_id smallint NOT NULL,
    logged_time timestamp without time zone DEFAULT LOCALTIMESTAMP NOT NULL
);
    DROP TABLE public.events;
       public         postgres    false            �            1259    16384    gates    TABLE     o   CREATE TABLE public.gates (
    id smallint NOT NULL,
    name text NOT NULL,
    openable boolean NOT NULL
);
    DROP TABLE public.gates;
       public         postgres    false            �            1259    24576    subscriptions    TABLE     �   CREATE TABLE public.subscriptions (
    user_id integer NOT NULL,
    gate_id smallint NOT NULL,
    type text NOT NULL,
    logged_time timestamp without time zone DEFAULT LOCALTIMESTAMP NOT NULL
);
 !   DROP TABLE public.subscriptions;
       public         postgres    false            �            1259    16390    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username text,
    authorized boolean,
    log_in timestamp without time zone DEFAULT LOCALTIMESTAMP NOT NULL,
    role text NOT NULL,
    name text NOT NULL
);
    DROP TABLE public.users;
       public         postgres    false            K          0    24591    events 
   TABLE DATA               @   COPY public.events (event_id, gate_id, logged_time) FROM stdin;
    public       postgres    false    199   L       H          0    16384    gates 
   TABLE DATA               3   COPY public.gates (id, name, openable) FROM stdin;
    public       postgres    false    196   i       J          0    24576    subscriptions 
   TABLE DATA               L   COPY public.subscriptions (user_id, gate_id, type, logged_time) FROM stdin;
    public       postgres    false    198   �       I          0    16390    users 
   TABLE DATA               M   COPY public.users (id, username, authorized, log_in, role, name) FROM stdin;
    public       postgres    false    197          �
           2606    24602    events events_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id, gate_id, logged_time);
 <   ALTER TABLE ONLY public.events DROP CONSTRAINT events_pkey;
       public         postgres    false    199    199    199            �
           2606    16398    gates gates_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.gates
    ADD CONSTRAINT gates_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.gates DROP CONSTRAINT gates_pkey;
       public         postgres    false    196            �
           2606    24580    subscriptions user_gate_pk 
   CONSTRAINT     f   ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT user_gate_pk PRIMARY KEY (user_id, gate_id);
 D   ALTER TABLE ONLY public.subscriptions DROP CONSTRAINT user_gate_pk;
       public         postgres    false    198    198            �
           2606    16400    users user_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_pkey;
       public         postgres    false    197            �
           2606    24603    events events_gates_fk    FK CONSTRAINT     u   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_gates_fk FOREIGN KEY (gate_id) REFERENCES public.gates(id);
 @   ALTER TABLE ONLY public.events DROP CONSTRAINT events_gates_fk;
       public       postgres    false    196    199    2757            �
           2606    24586    subscriptions gate_id_fk    FK CONSTRAINT     w   ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT gate_id_fk FOREIGN KEY (gate_id) REFERENCES public.gates(id);
 B   ALTER TABLE ONLY public.subscriptions DROP CONSTRAINT gate_id_fk;
       public       postgres    false    198    2757    196            �
           2606    24581    subscriptions user_id_fk    FK CONSTRAINT     w   ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES public.users(id);
 B   ALTER TABLE ONLY public.subscriptions DROP CONSTRAINT user_id_fk;
       public       postgres    false    197    198    2759            K      x������ � �      H   4   x�3�(M-*IT(��K�,H��L�2��/*��S0�,�2�q���=... ���      J   R   x��λ� �U�`t'>��8��ؙS���,���&�w�DEdE�x��}6+��.=AW�)�*�����6�,W��l3�      I   �   x�]�=�0@��9E/�(����)��XJ�
hK�H�=�߇������x��Pk���"ά9���hmF�~�1F#sY�S!�Q���e��K�D�,�+�29�Ȫ��Cw�nk���9�d&���fw�ιT-<     