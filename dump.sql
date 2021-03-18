--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6
-- Dumped by pg_dump version 12.6

-- Started on 2021-02-17 13:52:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16396)
-- Name: forum; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forum (
    id integer NOT NULL,
    name text NOT NULL,
    short_name text,
    creator_user_id integer NOT NULL
);


ALTER TABLE public.forum OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16394)
-- Name: forum_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forum_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.forum_id_seq OWNER TO postgres;

--
-- TOC entry 2859 (class 0 OID 0)
-- Dependencies: 202
-- Name: forum_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forum_id_seq OWNED BY public.forum.id;


--
-- TOC entry 205 (class 1259 OID 16413)
-- Name: post; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.post (
    id integer NOT NULL,
    message text,
    creator_user_id integer NOT NULL,
    date date,
    thread_id integer NOT NULL
);


ALTER TABLE public.post OWNER TO postgres;

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_id_seq OWNER TO postgres;

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;

--
-- TOC entry 206 (class 1259 OID 16421)
-- Name: thread; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.thread (
    id integer NOT NULL,
    name text,
    creator_user_id integer NOT NULL,
    date date,
    message text,
    forum_id integer NOT NULL
);


ALTER TABLE public.thread OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16405)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name text,
    email text,
    username text NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 2703 (class 2604 OID 16399)
-- Name: forum id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum ALTER COLUMN id SET DEFAULT nextval('public.forum_id_seq'::regclass);


--
-- TOC entry 2850 (class 0 OID 16396)
-- Dependencies: 203
-- Data for Name: forum; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.forum (id, name, short_name, creator_user_id) FROM stdin;
\.


--
-- TOC entry 2852 (class 0 OID 16413)
-- Dependencies: 205
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.post (id, message, creator_user_id, date, thread_id) FROM stdin;
\.


--
-- TOC entry 2853 (class 0 OID 16421)
-- Dependencies: 206
-- Data for Name: thread; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.thread (id, name, creator_user_id, date, message, forum_id) FROM stdin;
\.


--
-- TOC entry 2851 (class 0 OID 16405)
-- Dependencies: 204
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, name, email, username) FROM stdin;
\.


--
-- TOC entry 2860 (class 0 OID 0)
-- Dependencies: 202
-- Name: forum_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_id_seq', 1, false);


--
-- TOC entry 2705 (class 2606 OID 16404)
-- Name: forum forum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum
    ADD CONSTRAINT forum_pkey PRIMARY KEY (id);


--
-- TOC entry 2715 (class 2606 OID 16420)
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- TOC entry 2717 (class 2606 OID 16428)
-- Name: thread thread_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thread
    ADD CONSTRAINT thread_pkey PRIMARY KEY (id);


--
-- TOC entry 2707 (class 2606 OID 16430)
-- Name: forum u_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum
    ADD CONSTRAINT u_name UNIQUE (name);


--
-- TOC entry 2709 (class 2606 OID 16432)
-- Name: forum u_short_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum
    ADD CONSTRAINT u_short_name UNIQUE (short_name);


--
-- TOC entry 2711 (class 2606 OID 16449)
-- Name: user u_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT u_username UNIQUE (username);


--
-- TOC entry 2713 (class 2606 OID 16412)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2722 (class 2606 OID 16455)
-- Name: thread forum_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thread
    ADD CONSTRAINT forum_fk FOREIGN KEY (forum_id) REFERENCES public.forum(id) NOT VALID;


--
-- TOC entry 2720 (class 2606 OID 16450)
-- Name: post thread_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT thread_fk FOREIGN KEY (thread_id) REFERENCES public.thread(id) NOT VALID;


--
-- TOC entry 2718 (class 2606 OID 16433)
-- Name: forum user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum
    ADD CONSTRAINT user_fk FOREIGN KEY (creator_user_id) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2719 (class 2606 OID 16438)
-- Name: post user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT user_fk FOREIGN KEY (creator_user_id) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2721 (class 2606 OID 16443)
-- Name: thread user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thread
    ADD CONSTRAINT user_fk FOREIGN KEY (creator_user_id) REFERENCES public."user"(id) NOT VALID;


-- Completed on 2021-02-17 13:52:49

--
-- PostgreSQL database dump complete
--

